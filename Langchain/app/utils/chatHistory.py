from typing import List, Dict
from langchain_core.messages import HumanMessage, AIMessage


class ChatHistory:
    
    @staticmethod
    def parse_conversations(messagesList: List[Dict[str,any]]) -> List[Dict[str, any]]:
        """
        Parsea mensajes alternados (user, llm, user, llm, ...) 
        en pares pregunta-respuesta.
        
        """
        conversations = []
        i = 0
        
        while i < len(messagesList) - 1:
            if messagesList[i]["is_user_message"] and not messagesList[i + 1]["is_user_message"]:
                conversations.append({
                    "user_question": messagesList[i]["text"],
                    "llm_response": messagesList[i + 1]["text"],
                })
                i += 2
            else:
                i += 1
        
        return conversations
    
    @staticmethod
    def getChatHistory(conversations: List[Dict[str, any]]) ->   List[Dict[str, any]]:
        """
        Convierte pares pregunta-respuesta a HumanMessage/AIMessage.

        """
        messages = []
        for conv in conversations:
            messages.append(HumanMessage(content=conv["user_question"]))
            messages.append(AIMessage(content=conv["llm_response"]))
        return messages


