import os
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings

load_dotenv()
api_key=os.environ["GOOGLE_API_KEY"] ##Modificar para produccion


embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001", google_api_key= api_key)

def get_document_embedding(text: list[str]) -> list[list[float]]:
    
    return embeddings.embed_documents(texts=text, task_type="SEMANTIC_SIMILARITY", output_dimensionality=128)
    ##SEMANTIC_SIMILARITY : incrustaciones optimizadas para evaluar la similitud del texto.


embedding = get_document_embedding("Hello, world!")
print(embedding[0])