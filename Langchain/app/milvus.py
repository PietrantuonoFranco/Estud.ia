from pymilvus import MilvusClient, DataType
from fastapi import FastAPI
from typing import Optional
from dotenv import load_dotenv
import os

load_dotenv()  
uri = os.getenv("MILVUS_URI")


##Funciones Milvus
def milvus_client(uri: str , db_name: Optional[str] = None) -> MilvusClient:
    """Instancia un cliente de Milvus con la URI (del contenedor) y la base de datos especificada. 
    Si no se especifica db_name, se conecta al cliente sin base de datos."""
    
    if not db_name:
        client = MilvusClient(
            uri = uri,
        )
        
    
    client = MilvusClient(
        uri = uri,
        db_name= db_name 
        
    )
    
    return client

def create_database(db : str, client : MilvusClient):
    
    """Crea una base de datos en Milvus si no existe. Aca el cliente debe ser instanciado sin base de datos."""
    
    if db not in client.list_databases():
        
        client.create_database(db)
    else:
        print(f"La base de datos {db} ya existe")
        
    
def create_milvus_collection(name: str, client : MilvusClient):
    
    """"Crea una coleccion en Milvus con el esquema e indices definidos."""
    
    if name in client.list_collections():
        
        print(f"La coleccion {name} ya existe")
        return None
    
    # <-- Esquema -->
    schema = MilvusClient.create_schema(
        auto_id=True,
        enable_dynamic_field=True,
    )

    schema.add_field(field_name="id", datatype=DataType.INT64, is_primary=True, auto_id=True)
    schema.add_field(field_name="vector_chunk", datatype=DataType.FLOAT_VECTOR, dim=1536) ##dim 1536 | recomendada para Gemini
    schema.add_field(field_name="text_chunk", datatype=DataType.VARCHAR, max_length=2000)
    schema.add_field(field_name="metadata", datatype=DataType.JSON, nullable=True) ##Datos adicionales que sirven para filtrar la busqueda

    ## <-- Indices -->
    index_params = client.prepare_index_params()


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
    

    collection = client.create_collection(
        collection_name=name,
        schema=schema,
        index_params=index_params
    )

    ##Cargamos la coleccion en memoria
    res = client.get_load_state(
        collection_name=name
    )

    print(res)


def remove_collection(name_collection: str, client : MilvusClient ) : 
    
    client.drop_collection(
        collection_name=name_collection
    )


def upload_document(data: list[dict], collection_name : str, client : MilvusClient ):
    
    res = client.insert(
        collection_name = collection_name,
        data = data
    )
    
    print(f"resultado de la insercion: {res}, en la coleccion: {collection_name}")


def get_document(query_vector: list[float], collection_name: str,filter : str, client : MilvusClient ) :
    
    res = client.search(
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
    

##Crear base de datos 
client_universal = milvus_client( uri = uri)
create_database("estudia_db",client_universal)
##Instanciamos cliente con base de datos
client_db = milvus_client( uri = uri , db_name= "estudia_db")
##Crear coleccion en estudia_db
create_milvus_collection("documents_collection", client_db)




##Endpoints FastAPI

app = FastAPI()

@app.post("/upload_document")
def upload_document_endpoint(data: list[dict], collection_name : str ):
    upload_document(data, collection_name)
    return {"message": "Document uploaded successfully"}

@app.get("/get_document")
def get_document_endpoint(query_vector: list[float], collection_name: str, filter: str):
    get_document( query_vector, collection_name, filter)
    return {"message": "Document retrieved successfully"}