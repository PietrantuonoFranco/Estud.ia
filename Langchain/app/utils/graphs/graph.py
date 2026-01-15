from typing import TypedDict, Annotated, Literal
from langgraph.graph import StateGraph, END
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.chat_models import init_chat_model
import operator
import json

from ..embbedings import EmbeddingGenerator
from ..reranker import Reranker
from ...db.milvus import Async_Milvus_Client

##Clase estado del grafo
class RAGState(TypedDict):
    """Estado del grafo RAG con validación"""
    question: str  # Pregunta original
    query: str  # Query refinada (puede cambiar)
    context: str  # Contexto recuperado
    pdf_ids: list[int]  # IDs de los PDFs utilizados como contexto
    generation: str  # Respuesta generada
    is_valid: bool  # Si la respuesta es válida según el judge
    refinement_attempts: Annotated[int, operator.add]  # Contador de intentos
    retrieval_attempts: Annotated[int, operator.add]  # Contador de retrieves


class RAGGraph:
   
    
    def __init__(self, embedding_generator: EmbeddingGenerator, reranker: Reranker, client_milvus:Async_Milvus_Client):
        """
        Inicializar el grafo RAG
        
        Args:
            embedding_generator: Generador de embeddings para queries
            reranker: Reranker para ordenar resultados
            client_milvus: Cliente asíncrono de Milvus
        """
        self.embedding_generator = embedding_generator
        self.reranker = reranker
        self.client_milvus = client_milvus
        self.workflow = None
        self.app = None
    
    async def retrieve_context(self, state: RAGState) -> RAGState:
        """
        Nodo 1: Recupera contexto de Milvus directamente
        """
        print(f"\n [RETRIEVE] Buscando contexto para: '{state['query']}'")
        
        try:
            # Generar embedding de la query
            query_vector = await self.embedding_generator.get_query_embedding(text=state["query"])
            
            # Obtener documentos de Milvus
            results = await self.client_milvus.get_document(
                query_vector=query_vector, 
                collection_name="documents_collection", 
                ids=state["pdf_ids"]
            )
            
            # Reranking
            context = self.reranker.rerank(query=state["query"], document=[results])
            
            # Convertir a string si es necesario
            context = str(context) if not isinstance(context, str) else context
            
        except Exception as e:
            context = f"Error al recuperar contexto: {str(e)}"
            print(f"   Error: {str(e)}")
        
        return {
            **state,
            "context": context,
            "retrieval_attempts": 1
        }

    async def generate_answer(self, state: RAGState) -> RAGState:
        """
        Nodo 2: Genera respuesta usando el contexto
        """
        print("\n  [GENERATE] Generando respuesta...")
        
        model = init_chat_model("google_genai:gemini-2.5-flash-lite")
        
        generator_prompt = ChatPromptTemplate.from_messages([
            ("system", """Eres un asistente/profesor útil y conciso que ayuda a los usuarios a estudiar usando **únicamente** el PDF previamente subido como contexto.  

- Usa exclusivamente la información presente en `{context}`.  
- **No inventes** información. Si la respuesta no puede responderse con lo provisto, responde exactamente: "No puedo responder eso con la información provista." y, si es posible, sugiere 1–2 acciones para obtener la respuesta.
- **No reveles razonamiento interno** (no escribir chain-of-thought). En lugar de eso, entrega:  
  1) **Respuesta** — respuesta clara y directa (1–3 frases);  
  2) **Justificación en base al texto** — hasta 3 bullets que indiquen qué partes del `{context}` sustentan la respuesta;"""),
            ("human", "{question}")
        ])
        
        generator_chain = generator_prompt | model | StrOutputParser() ##chain
        
        generation = await generator_chain.ainvoke({
            "context": state["context"],
            "question": state["question"]
        })
        
        return {
            **state,
            "generation": generation
        }

    async def judge_answer(self, state: RAGState) -> RAGState:
        """
        Nodo 3: LLM as Judge - Evalúa si la respuesta es buena usando un modelo más grande
        """
        print("\n  [JUDGE] Evaluando calidad de la respuesta...")
        
        # Usar un modelo más grande para juzgar
        judge_model = init_chat_model("google_genai:gemini-2-pro")
        
        judge_prompt = ChatPromptTemplate.from_messages([
            ("system", """Eres un juez experto que evalúa si una respuesta es de buena calidad.

Analiza si:
1. La respuesta está fundamentada en el contexto proporcionado
2. La respuesta es precisa y relevante a la pregunta
3. La respuesta no contiene información inventada fuera del contexto
4. Si dice "No puedo responder...", determina si es una respuesta válida a falta de información

Responde con un JSON con este formato EXACTO:
{
    "is_valid": true/false,
    "reasoning": "explicación breve"
}

NO agregues más texto, SOLO el JSON."""),
            ("human", """Pregunta: {question}

Contexto: {context}

Respuesta: {generation}

¿Es una buena respuesta?""")
        ])
        
        try:
            result = await judge_model.ainvoke(judge_prompt.format(
                question=state["question"],
                context=state["context"],
                generation=state["generation"]
            ))
            
            # Parsear respuesta JSON
            result_json = json.loads(result)
            is_valid = result_json.get("is_valid", False)
            reasoning = result_json.get("reasoning", "")
            
            print(f"  Veredicto: {' Válida' if is_valid else ' Inválida'} - {reasoning}")
        except Exception as e:
            print(f"  Error en evaluación: {str(e)}")
            is_valid = True  # Si falla el judge, aceptar la respuesta
        
        return {
            **state,
            "is_valid": is_valid
        }

    async def refine_query(self, state: RAGState) -> RAGState:
        """
        Nodo 4: Refina la query cuando la respuesta es inválida
        """
        print("\n [REFINE] Refinando query para obtener mejor contexto...")
        
        model = init_chat_model("google_genai:gemini-2.5-flash-lite")
        
        refiner_prompt = ChatPromptTemplate.from_messages([
            ("system", """Eres un experto en reformular preguntas para mejorar la recuperación de información.

La pregunta original no obtuvo una respuesta satisfactoria. Reformúlala usando:
- Sinónimos más específicos
- Términos técnicos relevantes
- Diferentes ángulos de la pregunta
- Descomposición en sub-preguntas si es necesario

Responde SOLO con la pregunta reformulada, sin explicaciones adicionales."""),
            ("human", "Pregunta original: {question}\n\nRespuesta insatisfactoria: {generation}")
        ])
        
        refiner_chain = refiner_prompt | model | StrOutputParser()
        
        refined_query = await refiner_chain.ainvoke({
            "question": state["question"],
            "generation": state["generation"]
        })
        
        print(f"  Query refinada: '{refined_query}'")
        
        return {
            **state,
            "query": refined_query,
            "refinement_attempts": 1
        }

    async def should_refine(self, state: RAGState) -> Literal["refine", "end"]:
        """
        Nodo de decisión: ¿Refinar y reintentar o terminar?
        """
        max_refinements = 2
        
        if not state["is_valid"] and state["refinement_attempts"] < max_refinements:
            print(f"\n [DECISION] Refinando (Intento {state['refinement_attempts']}/{max_refinements})")
            return "refine"
        else:
            if state["is_valid"]:
                print("\n [DECISION] Respuesta validada, terminando")
            else:
                print(f"\n [DECISION] Máximos intentos de refinamiento alcanzados, terminando")
            return "end"

    def build(self):
        """
        Construye y compila el grafo
        """
        self.workflow = StateGraph(RAGState)
        
        # Agregar nodos (ahora son métodos de la clase)
        self.workflow.add_node("retrieve", self.retrieve_context)
        self.workflow.add_node("generate", self.generate_answer)
        self.workflow.add_node("judge", self.judge_answer)
        self.workflow.add_node("refine", self.refine_query)
        
        # Definir flujo
        self.workflow.set_entry_point("retrieve")
        self.workflow.add_edge("retrieve", "generate")
        self.workflow.add_edge("generate", "judge")
        self.workflow.add_conditional_edges(
            "judge",
            self.should_refine,
            {
                "refine": "refine",
                "end": END
            }
        )
        self.workflow.add_edge("refine", "retrieve")
        
        # Compilar
        self.app = self.workflow.compile()
        
        return self.app
    
    async def invoke(self, initial_state: RAGState):
        """
        Invoca el grafo con un estado inicial
        """
        if self.app is None:
            self.build()
        
        return await self.app.ainvoke(initial_state)


# Patron builder, crea el el objeto RAGGraph y construye el grafo (objeto) dentro de el atributo workflow
def create_rag_graph(embedding_generator: EmbeddingGenerator, reranker: Reranker, client_milvus:Async_Milvus_Client):
    """
    Factory function que crea una instancia de RAGGraph y construye el grafo
    
    Args:
        embedding_generator: Generador de embeddings
        reranker: Reranker de resultados
        client_milvus: Cliente asíncrono de Milvus
    """
    rag_graph = RAGGraph(embedding_generator, reranker, client_milvus)
    rag_graph.build()
    return rag_graph
