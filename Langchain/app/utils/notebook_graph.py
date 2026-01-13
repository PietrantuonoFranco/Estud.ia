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
    pdfs_ids: list[int]  # IDs de los PDFs subidos
    context: str  # Contexto recuperado de todos los PDFs
    generation: str  # JSON generado con title, icon y description

class NotebookGraph:
    """
    Grafo para la creación de notebooks basado en un PDF
    """

    START: Literal["start"] = "start"
    END: Literal["end"] = "end"

    def __init__(self, embedding_generator: EmbeddingGenerator, client_milvus: Async_Milvus_Client):
        """
        Inicializa el grafo con los nodos y transiciones necesarias
        """
        self.embedding_generator = embedding_generator
        self.client_milvus = client_milvus
        self.workflow = None
        self.app = None

    async def retrieve_context(self, state: NotebookGraphState) -> NotebookGraphState:
        """
        Recupera todo el contexto de uno o más PDFs automáticamente.
        Se obtienen los fragmentos más representativos de cada documento para su análisis.
        """

        pdf_ids = state.get('pdfs_ids', [])
        print(f"\n [RETRIEVE] Recuperando contexto de {len(pdf_ids)} PDF(s): {pdf_ids}")
        
        all_contexts = []
        
        try:
            # Query genérica para obtener una visión general del documento
            generic_query = "Contenido principal y temas del documento"
            
            # Generar embedding de la query genérica
            query_vector = await self.embedding_generator.get_query_embedding(text=generic_query)
            
            # Iterar sobre cada PDF ID y recuperar su contexto
            for pdf_id in pdf_ids:
                print(f"   [RETRIEVE] Procesando PDF ID: {pdf_id}")
                
                # Filtrar por pdf_id específico
                filter_expr = f'pdf_id == {pdf_id}'
                
                results = await self.client_milvus.get_document(
                    query_vector=query_vector, 
                    collection_name="documents_collection", 
                    filter=filter_expr
                )
                
                # Procesar resultados de este PDF
                if isinstance(results, list) and len(results) > 0:
                    pdf_context = "\n\n".join([str(doc) for doc in results])
                    all_contexts.append(f"--- Documento {pdf_id} ---\n{pdf_context}")
                    print(f"   [RETRIEVE] Recuperados {len(results)} fragmentos del PDF {pdf_id}")
                elif isinstance(results, list) and len(results) == 0:
                    print(f"   [RETRIEVE] No se encontraron documentos para pdf_id: {pdf_id}")
                else:
                    if results:
                        all_contexts.append(f"--- Documento {pdf_id} ---\n{str(results)}")
            
            # Combinar todos los contextos
            context = "\n\n".join(all_contexts) if all_contexts else ""
            print(f"   [RETRIEVE] Contexto total: {len(context)} caracteres")
            
        except Exception as e:
            context = ""
            print(f"   [RETRIEVE] Error: {str(e)}")
        
        return {
            **state,
            "context": context
        }

    async def generate_notebook(self, state: NotebookGraphState) -> NotebookGraphState:
        """
        Genera automáticamente los metadatos del notebook (title, icon, description) basándose en el PDF.
        """
        print("\n  [GENERATE] Generando metadatos del notebook...")
        
        # Validar que haya contexto disponible
        context = state.get("context", "").strip()
        print(f"\n  [GENERATE] Longitud del contexto: {len(context)} caracteres")
        
        if not context:
            error_json = '{"message": "No puedo realizar la acción con la información provista."}'
            print(f"\n  [GENERATE] Error: No se encontró contexto para el PDF")
            return {
                **state,
                "generation": error_json
            }
        
        model = init_chat_model("google_genai:gemini-2.5-flash-lite")
        
        generator_prompt = ChatPromptTemplate.from_messages([
            ("user", """Eres un agente especializado en analizar documentos PDF y generar metadatos para notebooks automáticamente.

Tu tarea es analizar el contenido de uno o más documentos y generar ÚNICAMENTE un JSON válido con los siguientes campos:
- title: Título conciso que refleje el contenido principal de los documentos (máximo 255 caracteres, sin comillas ni detalles excesivos)
- icon: Un emoji representativo del tema de los documentos
- description: Descripción clara y concisa del contenido (máximo 1024 caracteres)

Instrucciones obligatorias:
1. Si hay múltiples documentos, crea un título y descripción que unifique sus temas
2. Usa EXCLUSIVAMENTE la información del contexto proporcionado
3. NO inventes información que no esté en los documentos
4. Si el contenido es insuficiente o inadecuado, devuelve: {{"message": "No puedo realizar la acción con la información provista."}}
5. Responde SOLO con el JSON, sin texto adicional ni explicaciones
6. El JSON debe ser válido y poder parsearse directamente

Contexto de los documentos:
{context}

Responde únicamente con el JSON:""")
        ])
        
        generator_chain = generator_prompt | model | StrOutputParser()
        
        print(f"\n  [GENERATE] Invocando modelo con contexto de {len(context)} caracteres")
        
        generation = await generator_chain.ainvoke({
            "context": context
        })
        
        print(f"\n  [GENERATE] Resultado: {generation[:200]}...")
        
        return {
            **state,
            "generation": generation
        }

    def build(self):
        """
        Construye y compila el grafo
        """
        self.workflow = StateGraph(NotebookGraphState)
        
        # Agregar nodos (ahora son métodos de la clase)
        self.workflow.add_node("retrieve", self.retrieve_context)
        self.workflow.add_node("generate", self.generate_notebook)
        
        # Definir flujo
        self.workflow.set_entry_point("retrieve")
        self.workflow.add_edge("retrieve", "generate")
        self.workflow.add_edge("generate", END)

        
        # Compilar
        self.app = self.workflow.compile()
        
        return self.app
    
    async def invoke(self, initial_state: NotebookGraphState):
        """
        Invoca el grafo con un estado inicial
        """
        if self.app is None:
            self.build()
        
        return await self.app.ainvoke(initial_state)


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