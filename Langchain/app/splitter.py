from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader


##Función para generar chunks de texto
def splitter(file_path:str):
    
    """Divide un texto en fragmentos más pequeños utilizando RecursiveCharacterTextSplitter."""
    
    if file_path:
        loader = PyPDFLoader(file_path)
        docs = loader.load() ##Crea un documento por pagina del PDF
    
    text_splitter = RecursiveCharacterTextSplitter( ##Recibe solo objeto del tipo Document
        chunk_size=1000,  # Tamaño del chunk (caracteres)
        chunk_overlap=200,  
        add_start_index=True,  
    )
    
    all_splits = text_splitter.split_documents(docs)
    return all_splits


##Ejemplo de uso con PDF
chunks = splitter(file_path = "C:/Users/ivija/Desktop/Estud.ia/Langchain/app/bitcoin_es.pdf")
print(chunks[0].page_content) ##Imprime el contenido del primer chunk