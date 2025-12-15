import os
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings

load_dotenv()
api_key=os.environ["GOOGLE_API_KEY"] ##Modificar para produccion



class EmbeddingGenerator:
    
    
    def __init__(self):
        self.embeddings =  GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001", google_api_key= api_key)
    
    async def get_document_embedding(self,text: list[str]) -> list[list[float]]:
        
        """Genera embeddings para una lista de textos (documentos)"""
        """Un embedding por string en la lista"""        
        
        return await self.embeddings.aembed_documents(texts=text, task_type="RETRIEVAL_DOCUMENT", output_dimensionality=3072 )
    
        ##SEMANTIC_SIMILARITY : incrustaciones optimizadas para evaluar la similitud del texto.
        ##La dim 3072 ya esta normalizada


    async def get_query_embedding(self,text: str) -> list[float]:
        
        return await self.embeddings.aembed_query(text=text, task_type="SEMANTIC_SIMILARITY", output_dimensionality=3072 )

    
    def format_database (self, text_chunks:list[dict], vector_chunks:list[list[float]] ):
        """Formatea los chunks de texto y sus embeddings en una lista de diccionarios para insertar en la base de datos.
        """
        
        formatted_data = []
        
        for i , j in zip(text_chunks, vector_chunks):
            data = {
                "text_chunk": i['text'],
                "metadata": i['metadata'],
                "vector_chunk": j
            }
            formatted_data.append(data)
        
        return formatted_data





##embedding = EmbeddingGenerator()
##doc_embedding = embedding.get_document_embedding(["Falopatina es la mejor materia"])
##print(f"doc_embedding:",doc_embedding)

##query_embedding = embedding.get_query_embedding("Hello, world!")
##print(f"query_embedding:",query_embedding)