from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Literal
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.chat_models import init_chat_model

from .embbedings import EmbeddingGenerator
from ..db.milvus import Async_Milvus_Client


class NotebookGraphState(TypedDict):
    """
    Estado del grafo para la creación de notebooks
    """
    pdf_id: str  # ID del PDF subido (puede ser el nombre del archivo o un identificador)
    context: str  # Contexto recuperado del PDF completo
    generation: str  # JSON generado con title, icon y description
    is_valid: bool  # Si la respuesta es válida según el judge

class NotebookGraph(StateGraph[NotebookGraphState]):
    """
    Grafo para la creación de notebooks basado en un PDF
    """

    START: Literal["start"] = "start"
    END: Literal["end"] = "end"

    def __init__(self, embedding_generator: EmbeddingGenerator, client_milvus: Async_Milvus_Client):
        """
        Inicializa el grafo con los nodos y transiciones necesarias
        """
        super().__init__(initial_state={
            "pdf_id": "",
            "context": "",
            "generation": "",
            "is_valid": False
        })
        self.embedding_generator = embedding_generator
        self.client_milvus = client_milvus
        self.workflow = None
        self.app = None

    async def retrieve_context(self, state: NotebookGraphState) -> NotebookGraphState:
        """
        Recupera todo el contexto del PDF automáticamente sin necesidad de una query específica.
        Se obtienen los fragmentos más representativos del documento para su análisis.
        """

        print(f"\n [RETRIEVE] Recuperando contexto completo del PDF: '{state['pdf_id']}'")
        
        try:
            # Query genérica para obtener una visión general del documento
            generic_query = "Contenido principal y temas del documento"
            
            # Generar embedding de la query genérica
            query_vector = await self.embedding_generator.get_query_embedding(text=generic_query)
            
            # Obtener documentos de Milvus (se puede filtrar por pdf_id si está disponible)
            filter_expr = f'pdf_id == "{state["pdf_id"]}".strip()' if state.get("pdf_id") else ""
            
            results = await self.client_milvus.get_document(
                query_vector=query_vector, 
                collection_name="documents_collection", 
                filter=filter_expr,
                limit=10  # Obtener más fragmentos para mejor contexto
            )
            
            # Concatenar todos los resultados para tener contexto completo
            if isinstance(results, list):
                context = "\n\n".join([str(doc) for doc in results])
            else:
                context = str(results)
            
        except Exception as e:
            context = f"Error al recuperar contexto: {str(e)}"
            print(f"   Error: {str(e)}")
        
        return {
            **state,
            "context": context
        }

    async def generate_notebook(self, state: NotebookGraphState) -> NotebookGraphState:
        """
        Genera automáticamente los metadatos del notebook (title, icon, description) basándose en el PDF.
        """
        print("\n  [GENERATE] Generando metadatos del notebook...")
        
        model = init_chat_model("google_genai:gemini-2.5-flash-lite")
        
        generator_prompt = ChatPromptTemplate.from_messages([
            (
                "system", 
                """Eres un agente especializado en analizar documentos PDF y generar metadatos para notebooks automáticamente.

Tu tarea es analizar el contenido del documento y generar ÚNICAMENTE un JSON válido con los siguientes campos:
- title: Título conciso que refleje el contenido principal del documento (máximo 60 caracteres)
- icon: Un emoji representativo del tema del documento
- description: Descripción clara y concisa del contenido (máximo 512 caracteres)

Instrucciones obligatorias:
1. Usa EXCLUSIVAMENTE la información del contexto proporcionado
2. NO inventes información que no esté en el documento
3. Si el contenido es insuficiente o inadecuado, devuelve: {{"message": "No puedo realizar la acción con la información provista."}}
4. Responde SOLO con el JSON, sin texto adicional ni explicaciones
5. El JSON debe ser válido y poder parsearse directamente

Contexto del documento:
{context}

Responde únicamente con el JSON:""")
        ])
        
        generator_chain = generator_prompt | model | StrOutputParser()
        
        generation = await generator_chain.ainvoke({
            "context": state["context"]
        })
        
        print(f"\n  [GENERATE] Resultado: {generation[:200]}...")
        
        return {
            **state,
            "generation": generation
        }


def create_notebook_graph(embedding_generator: EmbeddingGenerator, client_milvus:Async_Milvus_Client):
    """
    Factory function que crea una instancia de NotebookGraph y construye el grafo
    
    Args:
        embedding_generator: Generador de embeddings
        client_milvus: Cliente asíncrono de Milvus
    """
    notebook_graph = NotebookGraph(embedding_generator, client_milvus)
    notebook_graph.build()
    return notebook_graph