from fastapi import FastAPI, UploadFile, File, Form, status, Security, HTTPException
import os
import shutil
import traceback
from contextlib import asynccontextmanager
from pydantic import BaseModel
from typing import List
import json

from .utils.embbedings import EmbeddingGenerator
from .utils.splitter import Splitter
from .db.milvus import Async_Milvus_Client
from .utils.reranker import Reranker
from .utils.graph import create_rag_graph
from .utils.notebook_graph import create_notebook_graph
from .security import verify_api_key

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

class SourceRequest(BaseModel):
    id: int
    file: UploadFile

class NotebookRequest(BaseModel):
    sources: list[SourceRequest]

class NotebookResponse(BaseModel):
    title: str
    icon: str
    description: str

##Inicializacion de objetos 
@asynccontextmanager
async def lifespan(app: FastAPI):
    
    ##Instancias de objetos (helpers)
    global splitter, embedding_generator, reranker, client_milvus, rag_graph, notebook_graph

    splitter = Splitter()
    embedding_generator = EmbeddingGenerator()
    reranker = Reranker()
    client_milvus = Async_Milvus_Client()
    
    ##Crear grafo RAG con dependencias locales (sin requests HTTP internos)
    rag_graph = create_rag_graph(
        embedding_generator=embedding_generator,
        reranker=reranker,
        client_milvus=client_milvus
    )
    
    # Crear grafo Notebook con dependencias locales
    notebook_graph = create_notebook_graph(
        embedding_generator=embedding_generator,
        client_milvus=client_milvus
    )
    
    yield
    
app = FastAPI(lifespan=lifespan, openapi_url="/api/v1")
    

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
            
            formatted_data = embedding_generator.format_database(text_chunks=text_chunks, vector_chunks=vector_chunks, pdf_id=file.filename)
            
            await client_milvus.upload_document(data=formatted_data, collection_name="documents_collection")
            
            return {"status": "success", "message": f"Document {file.filename} uploaded successfully", "chunks": len(texts)}
            
        finally:
            # Limpiar archivo temporal después de procesar
            if os.path.exists(file_path):
                os.remove(file_path)
        
    except Exception as e:
        traceback.print_exc()
        return {"error": str(e)}

@app.post("/upload-pdfs") 
async def upload_document_app(
    files: List[UploadFile] = File(...),
    source_ids: List[int] = Form(...),
    api_key: str = Security(verify_api_key)
):
    try:
        await upload_documents(files=files, source_ids=source_ids)

        return {"status": "success", "message": f"{len(files)} documents uploaded successfully", "source_ids": source_ids}
        
    except Exception as e:
        traceback.print_exc()
        return {"error": str(e)}



@app.get("/get_context") ## De prueba / depuracion 
async def get_context_app(request: ContextRequest, api_key: str = Security(verify_api_key) ):
    
    try:
        query_vector = await embedding_generator.get_query_embedding(text=request.query)
        
        results = await client_milvus.get_document(query_vector=query_vector, collection_name="documents_collection", filter="")
        
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
    

@app.post("/create-notebook", response_model=NotebookResponse)
async def create_notebook(
    files: List[UploadFile] = File(...),
    source_ids: List[int] = Form(...),
    api_key: str = Security(verify_api_key)
):
    """
    Endpoint para crear la información básica de un notebook en base a uno o más PDFs
    """
    try:
        await upload_documents(files=files, source_ids=source_ids)
        
        # Generar título, ícono y descripción usando el grafo
        initial_state = {
            "pdfs_ids": source_ids,
            "context": "",
            "generation": ""
        }

        result = await notebook_graph.invoke(initial_state)

        # Limpiar la respuesta de bloques de código markdown si existen
        generation_text = result["generation"].strip()
        if generation_text.startswith("```json"):
            generation_text = generation_text[7:]  # Remover ```json
        if generation_text.startswith("```"):
            generation_text = generation_text[3:]  # Remover ```
        if generation_text.endswith("```"):
            generation_text = generation_text[:-3]  # Remover ```
        generation_text = generation_text.strip()
            
        result_json = json.loads(generation_text)
            
        return NotebookResponse(
            title=result_json["title"],
            icon=result_json["icon"],
            description=result_json["description"]
        )
        
    except Exception as e:
        traceback.print_exc()
        
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while creating the notebook: {str(e)}"
        )
    
@app.post("/delete-pdfs", status_code=status.HTTP_200_OK)
async def delete_pdfs(request: dict, api_key: str = Security(verify_api_key)):
    """
    Endpoint para eliminar documentos PDF de la colección en Milvus.
    """
    try:
        pdf_ids = request.get("pdf_ids", [])
        
        if not pdf_ids or not isinstance(pdf_ids, list):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="pdf_ids must be a non-empty list"
            )
        
        res = await client_milvus.delete_documents(
            collection_name="documents_collection",
            ids=pdf_ids
        )
        
        if not res:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No documents were deleted. Please check the provided IDs."
            )

        return {"status": "success", "message": f"Documents with IDs {pdf_ids} deleted successfully"}
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while deleting the collection: {str(e)}"
        )
    

async def upload_documents(files: List[UploadFile] = File(...), source_ids: List[int] = Form(...)):
    """
    Función auxiliar para subir múltiples documentos PDF y procesarlos.
    """
    try:
        # Validar que haya la misma cantidad de archivos e IDs
        if len(files) != len(source_ids):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El número de archivos y source_ids debe coincidir"
            )
        
        # Guardar todos los archivos temporalmente
        for file in files:
            if not file.filename.endswith('.pdf'):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Only PDF files are allowed"
                )
            
            file_path = os.path.join(UPLOAD_DIRECTORY, file.filename)
            
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
        
        try:
            # Procesar cada archivo con su ID correspondiente
            for file, source_id in zip(files, source_ids):
                file_path = os.path.join(UPLOAD_DIRECTORY, file.filename)
                text_chunks = splitter.split_document(file_path=file_path)

                texts = [chunk['text'] for chunk in text_chunks]
            
                vector_chunks = await embedding_generator.get_document_embedding(text=texts)
            
                formatted_data = embedding_generator.format_database(text_chunks=text_chunks, vector_chunks=vector_chunks, pdf_id=source_id)
            
                await client_milvus.upload_document(data=formatted_data, collection_name="documents_collection")
        finally:
                # Limpiar archivos temporales después de procesar
                for file in files:
                    file_path = os.path.join(UPLOAD_DIRECTORY, file.filename)
                    if os.path.exists(file_path):
                        os.remove(file_path)
        
    except Exception as e:
        traceback.print_exc()
        
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while uploading documents: {str(e)}"
        )