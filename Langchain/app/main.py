from fastapi import FastAPI, UploadFile, File, status, Security
from .utils.embbedings import EmbeddingGenerator
from .utils.splitter import Splitter
from .db.milvus import upload_document, get_document
from .utils.reranker import Reranker
from .utils.graph import create_rag_graph
from .security import verify_api_key
import os
import shutil
import traceback
from contextlib import asynccontextmanager
from pydantic import BaseModel


UPLOAD_DIRECTORY = os.path.join(os.path.dirname(__file__), "uploaded_files")
os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)

class ContextRequest(BaseModel):
    query: str
    filter : str


class RAGRequest(BaseModel):
    question: str
    filter: str = ""


class RAGResponse(BaseModel):
    question: str
    generation: str
    context: str
    is_valid: bool
    refinement_attempts: int


##Inicializacion de objetos 
@asynccontextmanager
async def lifespan(app: FastAPI):
    
    ##Instancias de objetos (helpers)
    global splitter, embedding_generator, reranker, rag_graph
    splitter = Splitter()
    embedding_generator = EmbeddingGenerator()
    reranker = Reranker()
    
    ##Crear grafo RAG con dependencias locales (sin requests HTTP internos)
    rag_graph = create_rag_graph(
        embedding_generator=embedding_generator,
        reranker=reranker,
        get_document_func=get_document
    )
    
    
    yield
    
app = FastAPI(lifespan=lifespan)
    

@app.get("/")
def root():
    return {"message": "Langchain App is running"}

@app.get("/healthcheck", status_code=status.HTTP_200_OK)
async def healthcheck():
    return {"status": "ok", "message": "Service is healthy"}

@app.post("/upload_document") 
async def upload_document_app(file: UploadFile, api_key: str = Security(verify_api_key)):
    
    try:
        # Validar que sea un PDF
        if not file.filename.endswith('.pdf'):
            return {"error": "Only PDF files are allowed"}
        
        # Guardar temporalmente el archivo
        file_path = os.path.join(UPLOAD_DIRECTORY, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        try:
            # Procesar el documento
            text_chunks = splitter.split_document(file_path=file_path)
            texts = [chunk['text'] for chunk in text_chunks]
            
            vector_chunks = await embedding_generator.get_document_embedding(text=texts)
            
            formatted_data = embedding_generator.format_database(text_chunks=text_chunks, vector_chunks=vector_chunks)
            
            await upload_document(data=formatted_data, collection_name="documents_collection")
            
            return {"status": "success", "message": f"Document {file.filename} uploaded successfully", "chunks": len(texts)}
            
        finally:
            # Limpiar archivo temporal después de procesar
            if os.path.exists(file_path):
                os.remove(file_path)
        
    except Exception as e:
        traceback.print_exc()
        return {"error": str(e)}



@app.get("/get_context") ## De prueba / depuracion 
async def get_context_app(request: ContextRequest, api_key: str = Security(verify_api_key) ):
    
    try:
        query_vector = await embedding_generator.get_query_embedding(text=request.query)
        
        results = await get_document(query_vector=query_vector, collection_name="documents_collection", filter="")
        
        results_reranked = reranker.rerank(query=request.query, document=[results])
        
        return results_reranked
    
    except Exception as e:
        traceback.print_exc()
        return {"error": str(e)}


@app.post("/chat/rag", response_model=RAGResponse)
async def rag_endpoint(request: RAGRequest, api_key: str = Security(verify_api_key)):
    """
    Endpoint RAG con LangGraph - Valida respuesta con LLM as Judge
    y refina query si es necesario
    """
    try:
        
        
        # Estado inicial del grafo
        initial_state = {
            "question": request.question,
            "query": request.question,
            "context": "",
            "generation": "",
            "is_valid": False,
            "refinement_attempts": 0,
            "retrieval_attempts": 0
        }
        
        # Invocar el grafo (async wrapper on graph app)
        result = await rag_graph.invoke(initial_state)
        
       
        return RAGResponse(
            question=result["question"],
            generation=result["generation"],
            context=result["context"],
            is_valid=result["is_valid"],
            refinement_attempts=result["refinement_attempts"]
        )
        
    except Exception as e:
        traceback.print_exc()
        return {
            "error": str(e),
            "question": request.question,
            "generation": f"Error procesando la solicitud: {str(e)}",
            "context": "",
            "is_valid": False,
            "refinement_attempts": 0
        }