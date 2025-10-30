from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader


##Función para generar chunks de texto
def splitter_CharacterTextSplitter(file_path:str):
    
    """Divide un texto en Document, donde cada uno es una pagina del pdf. Luego divide cada Document en chunks de texto más pequeños.
        Retorna una lista de documentos (chunks)
    """
    
    if file_path:
        loader = PyPDFLoader(file_path)
        docs = loader.load() ##Crea un documento por pagina del PDF
    
    text_splitter = RecursiveCharacterTextSplitter( ##Recibe solo objeto del tipo Document
        chunk_size=1500,  # 1500 caracteres por chunk, aprox. seguro para 2,048 tokens del modelo Gemini que usamos en embeddings
        chunk_overlap=200,  
        add_start_index=True,  
        separators=["\n\n", "\n", ". ", "? ", "! ", " ", ""] ##Crea un nuevo chunk en el primer separador que encuentre
    )
    
    all_splits = text_splitter.split_documents(docs) ##Versione futuras, se podría tokenizar el texto !
    
    return all_splits
    



##Ejemplo de uso con PDF
path = "./bitcoin_es.pdf"
chunks = splitter_CharacterTextSplitter(file_path = path)
print(chunks[7])##Imprime el contenido del primer chunk