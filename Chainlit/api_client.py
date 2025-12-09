import requests
from dotenv import load_dotenv
import os


class Requests():
    def __init__(self):
    
        self.url_post = "http://langchain:3000/upload_document" ## Habría que ponerlos como env :)
        self.url_get = "http://langchain:3000/get_context"
        
    
    def request_upload_document_from_bytes(self, file_content: bytes, filename: str):
        """Envía un archivo PDF desde bytes (para usar con Chainlit)"""
        try:
            files = {'file': (filename, file_content, 'application/pdf')}
            response = requests.post(self.url_post, files=files, timeout=60)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"error": str(e)}
        
    def request_get_context(self, query: str, filter: str):
        """Envía una consulta al endpoint para obtener contexto"""
        try:
            
            response = requests.get(
                self.url_get,
                json={"query": query, "filter": filter},
                timeout=60
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"error": str(e)}
        

r = Requests()

#--> Upload <--
#result = r.request_upload_document("C:/Users/ivija/Desktop/Estud.ia/Langchain/app/bitcoin_es.pdf")
#print(result)
# -->Get Context <--
result = r.request_get_context(query="¿Qué es Bitcoin?", filter="")
print(result)