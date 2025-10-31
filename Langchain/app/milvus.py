from pymilvus import MilvusClient, DataType
from fastapi import FastAPI
from os import getenv

##Cliente Milvus
client = MilvusClient(
    uri = getenv("MILVUS_URI")
)

##App FastAPI
app = FastAPI()

   
#Db Creation
if "estud_ia_db" in client.list_databases():
    client.drop_database("estud_ia_db")
    client.create_database("estud_ia_db")
else:
    client.create_database("estud_ia_db")


 ##Funciones Milvus
def create_milvus_collection(name: str):
    
    """"Crea una coleccion en Milvus con el esquema e indices definidos."""
    # <-- Esquema -->
    schema = MilvusClient.create_schema(
        auto_id=False,
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
        field_name="source",
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


def remove_collection(name_collection: str):
    
    client.drop_collection(
        collection_name=name_collection
    )


def upload_document(data: list[dict], collection_name : str ):
    
    res = client.insert(
        collection_name = collection_name,
        data = data
    )
    
    print(f"resultado de la insercion: {res}, en la coleccion: {collection_name}")


def get_document(query_vector: list[float], collection_name: str,filter : str):
    
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
    

##Endpoints FastAPI
@app.post("/upload_document")
def upload_document_endpoint(data: list[dict], collection_name : str ):
    upload_document(data, collection_name)
    return {"message": "Document uploaded successfully"}

@app.get("/get_document")
def get_document_endpoint(query_vector: list[float], collection_name: str, filter: str):
    get_document( query_vector, collection_name, filter)
    return {"message": "Document retrieved successfully"}