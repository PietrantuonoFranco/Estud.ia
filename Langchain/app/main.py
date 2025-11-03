from fastapi import FastAPI, UploadFile, File
from .utils.embbedings import EmbeddingGenerator
from .utils.splitter import Splitter
from .db.milvus import upload_document, get_document
import os
from dotenv import load_dotenv
import shutil
import traceback
from contextlib import asynccontextmanager


UPLOAD_DIRECTORY = os.path.join(os.path.dirname(__file__), "uploaded_files")
os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)




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


