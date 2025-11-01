from pymilvus import MilvusClient, DataType
from fastapi import FastAPI
from typing import Optional
from dotenv import load_dotenv
from pydantic import BaseModel
import os

load_dotenv()  
uri = os.getenv("MILVUS_URI")



##Instancia del cliente Milvus

client = MilvusClient(
        uri = uri,
)

if "estudia_db" not in client.list_databases():
        
    client.create_database("estudia_db")
    
else:
    print(f"La base de datos {"estudia_db"} ya existe")

##Clienbte de estudia_db

client_db = MilvusClient(
        uri = uri,
        db_name= "estudia_db"
)
        
    
def create_milvus_collection(name: str):
    
    """"Crea una coleccion en Milvus con el esquema e indices definidos."""
    
    if name in client_db.list_collections():
        
        print(f"La coleccion {name} ya existe")
        return None
    
    # <-- Esquema -->
    schema = MilvusClient.create_schema(
        auto_id=True,
        enable_dynamic_field=True,
    )

    schema.add_field(field_name="id", datatype=DataType.INT64, is_primary=True, auto_id=True)
    schema.add_field(field_name="vector_chunk", datatype=DataType.FLOAT_VECTOR, dim=120) ##dim 1536 | recomendada para Gemini
    schema.add_field(field_name="text_chunk", datatype=DataType.VARCHAR, max_length=2000)
    schema.add_field(field_name="metadata", datatype=DataType.JSON, nullable=True) ##Datos adicionales que sirven para filtrar la busqueda

    ## <-- Indices -->
    index_params = client_db.prepare_index_params()


    index_params.add_index(
        field_name="vector_chunk", 
        index_type="HNSW",  ##Prepara un grafo con los vecinos mas cercanos | Pesadito (hay que evaluarlo)
        index_name="vector_index", 
        metric_type="COSINE",
        params={
            "M": 16, 
            "efConstruction": 256
        } 
    )
    
    index_params.add_index(
        field_name="text_chunk",
        index_type="INVERTED"  # Recomendado para VARCHAR
        
    )
    

    collection = client_db.create_collection(
        collection_name=name,
        schema=schema,
        index_params=index_params
    )

    ##Cargamos la coleccion en memoria
    res = client_db.get_load_state(
        collection_name=name
    )

    print(res)


def remove_collection(name_collection: str) : 
    
    client_db.drop_collection(
        collection_name=name_collection
    )


def upload_document(data: list[dict], collection_name : str,  ):
    
    res = client_db.insert(
        collection_name = collection_name,
        data = data
    )
    
    print(f"resultado de la insercion: {res}, en la coleccion: {collection_name}")


def get_document(query_vector: list[float], collection_name: str,filter : str) :
    
    res = client_db.search(
        collection_name=collection_name,
        anns_field = "vector_chunk",
        data = [query_vector],
        limit = 5,
        search_params={"metric_type":"COSINE"},
        filter = filter,
        output_fields = ["text_chunk"]
    )
    
    for hits in res:
        for hit in hits:
            print(hit)
    


##Crear coleccion en estudia_db
create_milvus_collection("documents_collection")




## FastAPI

class uploadDocumentRequest(BaseModel):
    data: list[dict]
    collection_name: str
    
class getDocumentRequest(BaseModel):
    query_vector: list[float]
    collection_name: str
    filter: str

app = FastAPI()

@app.post("/upload_document")
def upload_document_endpoint(request: uploadDocumentRequest):
    upload_document(request.data, request.collection_name)
    return {"message": "Document uploaded successfully"}

@app.get("/get_document")
def get_document_endpoint(request: getDocumentRequest):
    get_document( request.collection_name, request.query_vector, request.filter)
    return {"message": "Document retrieved successfully"}