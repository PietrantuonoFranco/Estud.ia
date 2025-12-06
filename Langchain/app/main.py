from fastapi import FastAPI, UploadFile, File, status
from .utils.embbedings import EmbeddingGenerator
from .utils.splitter import Splitter
from .db.milvus import upload_document, get_document
import os
from dotenv import load_dotenv
import shutil
import traceback
from contextlib import asynccontextmanager
from pydantic import BaseModel


UPLOAD_DIRECTORY = os.path.join(os.path.dirname(__file__), "uploaded_files")
os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)

class ContextRequest(BaseModel):
    query: str
    filter : str


##Inicializacion de objetos 
@asynccontextmanager
async def lifespan(app: FastAPI):
    
    ##Instancias de objetos (helpers)
    global splitter, embedding_generator
    splitter = Splitter()
    embedding_generator = EmbeddingGenerator()
    
    
    yield
    
app = FastAPI(lifespan=lifespan)
    

@app.get("/")
def root():
    return {"message": "Langchain App is running"}

@app.get("/healthcheck", status_code=status.HTTP_200_OK)
async def healthcheck():
    return {"status": "ok", "message": "Service is healthy"}

@app.post("/upload_document")
async def upload_document_app(file: UploadFile):
    
    try:
        file_path = os.path.join(UPLOAD_DIRECTORY, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        text_chunks = splitter.split_document(file_path=file_path)
        texts = [chunk['text'] for chunk in text_chunks]
        
        vector_chunks = embedding_generator.get_document_embedding(text=texts)
        
        formatted_data = embedding_generator.format_database(text_chunks=text_chunks, vector_chunks=vector_chunks)
        
        upload_document(data=formatted_data, collection_name="documents_collection")
        
    except Exception as e:
        return {"error": str(e)}



@app.get("/get_context")
def get_context_app(request: ContextRequest ):
    
    try:
        query_vector = embedding_generator.get_query_embedding(text=request.query)
        
        results = get_document(query_vector=query_vector, collection_name="documents_collection", filter="")
        
        contexts = [result.entity for result in results]
        
        return contexts
    
    except Exception as e:
        traceback.print_exc()
        return {"error": str(e)}