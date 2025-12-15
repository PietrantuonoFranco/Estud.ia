import requests
from typing import Optional, List, Dict, Any
import json
import os
from dotenv import load_dotenv


load_dotenv()
API_URL = os.getenv("API_URL")




class requests:
    """Cliente para interactuar con las API's creadas"""
    
    def __init__(self, base_url: str = API_URL):
        
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
    
    def upload_document(self, file_path: str) -> Dict[str, Any]:
        try:
            with open(file_path, 'rb') as file:
                files = {'file': (file_path.split('/')[-1], file, 'application/pdf')}
                response = self.session.post(
                    f"{self.base_url}/upload_document",
                    files=files
                )
                response.raise_for_status()
                return response.json() if response.text else {"status": "success"}
        except FileNotFoundError:
            return {"error": f"Archivo no encontrado: {file_path}"}
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}
    
    def get_context(self, query: str, filter: str = "") -> List[Dict[str, Any]]:
        try:
            # Nota: tu endpoint usa @app.get pero debería ser @app.post
            # porque estás enviando un body. Por ahora uso params
            params = {
                "query": query,
                "filter": filter
            }
            response = self.session.get(
                f"{self.base_url}/get_context",
                params=params
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}
    
    