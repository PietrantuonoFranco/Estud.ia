from langgraph.graph import StateGraph, END
from typing import TypedDict, Literal
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.chat_models import init_chat_model

from ..embbedings import EmbeddingGenerator
from ...db.milvus import Async_Milvus_Client


class CreationGraphState(TypedDict):
    """
    CreationGraph state for entities generation
    """
    option: str  # Entity type: "notebook", "source", "flashcard", "quiz"
    pdfs_ids: list[int]  # IDs of PDFs to analyze
    context: str  # Context recovered from all PDFs
    generation: str  # JSON generated with title, icon and description

class CreationGraph:
    """
    Graph for entity creation based on one or more PDFs
    """

    START: Literal["start"] = "start"
    END: Literal["end"] = "end"

    def __init__(self, embedding_generator: EmbeddingGenerator, client_milvus: Async_Milvus_Client):
        """
        Initializes the graph with the necessary nodes and transitions
        """
        self.embedding_generator = embedding_generator
        self.client_milvus = client_milvus
        self.workflow = None
        self.app = None

    async def retrieve_context(self, state: CreationGraphState) -> CreationGraphState:
        """
        Automatically retrieves all context from one or more PDFs.
        The most representative fragments of each document are obtained for analysis.
        """

        pdf_ids = state.get('pdfs_ids', [])
        print(f"\n [RETRIEVE] Retrieving context from {len(pdf_ids)} PDF(s): {pdf_ids}")
        
        all_contexts = []
        
        try:
            # Generic query to get an overview of the document
            generic_query = "Main content and topics of the document"
            
            # Generate embedding for the generic query
            query_vector = await self.embedding_generator.get_query_embedding(text=generic_query)
            
            # Iterate over each PDF ID and retrieve its context
            for pdf_id in pdf_ids:
                print(f"   [RETRIEVE] Processing PDF ID: {pdf_id}")
                
                # Filter by specific pdf_id
                filter_expr = f'pdf_id == {pdf_id}'
                
                results = await self.client_milvus.get_document(
                    query_vector=query_vector, 
                    collection_name="documents_collection", 
                    filter=filter_expr
                )
                
                # Process results for this PDF
                if isinstance(results, list) and len(results) > 0:
                    pdf_context = "\n\n".join([str(doc) for doc in results])
                    all_contexts.append(f"--- Document {pdf_id} ---\n{pdf_context}")
                    print(f"   [RETRIEVE] Retrieved {len(results)} fragments from PDF {pdf_id}")
                elif isinstance(results, list) and len(results) == 0:
                    print(f"   [RETRIEVE] No documents found for pdf_id: {pdf_id}")
                else:
                    if results:
                        all_contexts.append(f"--- Document {pdf_id} ---\n{str(results)}")
            
            # Combine all contexts
            context = "\n\n".join(all_contexts) if all_contexts else ""
            print(f"   [RETRIEVE] Total context length: {len(context)} characters")
            
        except Exception as e:
            context = ""
            print(f"   [RETRIEVE] Error: {str(e)}")
        
        return {
            **state,
            "context": context
        }

    async def generate_questions_and_answers(self, state: CreationGraphState) -> CreationGraphState:
        """
        Automatically generates 5 questions with their answers and 3 incorrect answers for quizzes.
        """
        print("\n  [GENERATE] Generating questions and answers...")
        
        # Validate that context is available
        context = state.get("context", "").strip()
        print(f"\n  [GENERATE] Context length: {len(context)} characters")
        
        if not context:
            error_json = '{"message": "I cannot perform the action with the provided information."}'
            print(f"\n  [GENERATE] Error: No context found for the PDF")
            return {
                **state,
                "generation": error_json
            }
        
        model = init_chat_model("google_genai:gemini-2.5-flash-lite")
        
        generator_prompt = ChatPromptTemplate.from_messages([
            ("user", """Eres un agente especializado en analizar documentos PDF y generar preguntas y respuestas para cuestionarios.

Tarea: Analiza los documentos adjuntos y genera exclusivamente un objeto JSON válido.

Estructura del JSON: Debe contener una única clave llamada "question_and_answers" cuyo valor sea un array de 5 objetos. Cada objeto debe tener:
- "question": Pregunta sobre el contenido (máximo 255 caracteres).
- "answer": Respuesta correcta detallada (máximo 255 caracteres).
- "incorrec_answer_1": Respuesta incorrecta plausible (máximo 255 caracteres).
- "incorrec_answer_2": Respuesta incorrecta plausible (máximo 255 caracteres).
- "incorrec_answer_3": Respuesta incorrecta plausible (máximo 255 caracteres).

Restricciones críticas:
- No incluyas introducciones, explicaciones ni bloques de código Markdown (como ```json).
- Solo devuelve el texto plano del JSON.
- Asegúrate de que los caracteres especiales estén escapados correctamente para no romper el formato JSON.
- La respuesta debe basarse estrictamente en los documentos proporcionados.
- Usa EXCLUSIVAMENTE la información del contexto proporcionado
- NO inventes información que no esté en los documentos
- Si el contenido es insuficiente o inadecuado, devuelve: {{"message": "No puedo realizar la acción con la información provista."}}
- El JSON debe ser válido y poder parsearse directamente

Contexto de los documentos:
{context}

Responde únicamente con el JSON:""")
        ])
        
        generator_chain = generator_prompt | model | StrOutputParser()
        
        print(f"\n  [GENERATE] Invoking model with context of {len(context)} characters")
        
        generation = await generator_chain.ainvoke({
            "context": context
        })
        
        print(f"\n  [GENERATE] Result: {generation[:200]}...")
        
        return {
            **state,
            "generation": generation
        }

    async def generate_notebook(self, state: CreationGraphState) -> CreationGraphState:
        """
        Generate notebook metadata (title, icon, description) automatically based on the PDF.
        """
        print("\n  [GENERATE] Generating notebook metadata...")
        
        # Validate that context is available
        context = state.get("context", "").strip()
        print(f"\n  [GENERATE] Context length: {len(context)} characters")
        
        if not context:
            error_json = '{"message": "I cannot perform the action with the provided information."}'
            print(f"\n  [GENERATE] Error: No context found for the PDF")
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
        
        print(f"\n  [GENERATE] Invoking model with context of {len(context)} characters")
        
        generation = await generator_chain.ainvoke({
            "context": context
        })
        
        print(f"\n  [GENERATE] Result: {generation[:200]}...")
        
        return {
            **state,
            "generation": generation
        }

    async def generate_flashcards(self, state: CreationGraphState) -> CreationGraphState:
        """
        Generate flashcards (questions and answers) automatically based on the PDF.
        """
        print("\n  [GENERATE] Generating flashcards...")
        
        # Validate that context is available
        context = state.get("context", "").strip()
        print(f"\n  [GENERATE] Context length: {len(context)} characters")
        
        if not context:
            error_json = '{"message": "I cannot perform the action with the provided information."}'
            print(f"\n  [GENERATE] Error: No context found for the PDF")
            return {
                **state,
                "generation": error_json
            }
        
        model = init_chat_model("google_genai:gemini-2.5-flash-lite")
        
        generator_prompt = ChatPromptTemplate.from_messages([
            ("user", """Eres un agente especializado en analizar documentos PDF y generar preguntas y respuestas para flashcards.

Tarea: Analiza los documentos adjuntos y genera exclusivamente un objeto JSON válido.

Estructura del JSON: Debe contener una única clave llamada "preguntas" cuyo valor sea un array de 5 objetos. Cada objeto debe tener:
- "question": Pregunta sobre el contenido (máximo 255 caracteres).
- "answer": Respuesta detallada (máximo 1024 caracteres).

Restricciones críticas:
- No incluyas introducciones, explicaciones ni bloques de código Markdown (como ```json).
- Solo devuelve el texto plano del JSON.
- Asegúrate de que los caracteres especiales estén escapados correctamente para no romper el formato JSON.
- La respuesta debe basarse estrictamente en los documentos proporcionados.
- Usa EXCLUSIVAMENTE la información del contexto proporcionado
- NO inventes información que no esté en los documentos
- Si el contenido es insuficiente o inadecuado, devuelve: {{"message": "No puedo realizar la acción con la información provista."}}
- El JSON debe ser válido y poder parsearse directamente

Contexto de los documentos:
{context}

Responde únicamente con el JSON:""")
        ])
        
        generator_chain = generator_prompt | model | StrOutputParser()
        
        print(f"\n  [GENERATE] Invoking model with context of {len(context)} characters")
        
        generation = await generator_chain.ainvoke({
            "context": context
        })
        
        print(f"\n  [GENERATE] Result: {generation[:200]}...")
        
        return {
            **state,
            "generation": generation
        }

    def route_to_generator(self, state: CreationGraphState) -> str:
        """
        Routes to the appropriate generator based on the option
        """
        option = state.get("option", "")
        print(f"\n  [ROUTE] Routing to: {option}")
        return option

    def build(self):
        """
        Builds and compiles the graph
        """
        self.workflow = StateGraph(CreationGraphState)
        
        # Add all nodes
        self.workflow.add_node("retrieve", self.retrieve_context)
        self.workflow.add_node("questions_and_answers", self.generate_questions_and_answers)
        self.workflow.add_node("notebook", self.generate_notebook)
        self.workflow.add_node("flashcards", self.generate_flashcards)
        
        # Define flow
        self.workflow.set_entry_point("retrieve")
        
        # Add conditional routing from retrieve to the appropriate generator
        self.workflow.add_conditional_edges(
            "retrieve",
            self.route_to_generator,
            {
                "questions_and_answers": "questions_and_answers",
                "notebook": "notebook",
                "flashcards": "flashcards"
            }
        )
        
        # Each generator goes to END
        self.workflow.add_edge("questions_and_answers", END)
        self.workflow.add_edge("notebook", END)
        self.workflow.add_edge("flashcards", END)
        
        # Compile
        self.app = self.workflow.compile()
        
        return self.app
    
    async def invoke(self, initial_state: CreationGraphState):
        """
        Invokes the graph with an initial state
        """
        if self.app is None:
            self.build()
        
        return await self.app.ainvoke(initial_state)


def create_creation_graph(embedding_generator: EmbeddingGenerator, client_milvus:Async_Milvus_Client):
    """
    Factory function that creates an instance of CreationGraph and builds the graph
    
    Args:
        embedding_generator: Embedding generator
        client_milvus: Asynchronous Milvus client
    """
    creation_graph = CreationGraph(embedding_generator, client_milvus)
    creation_graph.build()
    return creation_graph