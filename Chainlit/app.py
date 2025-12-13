from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import Runnable, RunnableConfig
from typing import cast

import chainlit as cl

import os
from config import conf
from langchain.chat_models import init_chat_model

from api_client import Requests
from dotenv import load_dotenv



os.environ["GOOGLE_API_KEY"] = conf.GOOGLE_API_KEY


@cl.on_chat_start
async def on_chat_start():

    ##Instancia del API Client de nuestros endpoints
    r = Requests()
    
    ##Pedimos PDF al usuario
    files = await cl.AskFileMessage(
        content="Porfavor suba un pdf, para arrancar la conversacion!", accept=["application/pdf"]
    ).send()
        
    if files: 
        file = files[0]
        
        print(file.path)

        msg = cl.Message(content=f"Procesando el archivo `{file.name}`, porfavor espere...")
        await msg.send()
        
        ##Leer el contenido del archivo y enviarlo al API
        with open(file.path, 'rb') as f:
            file_content = f.read()
        
        result = r.request_upload_document_from_bytes(
            file_content=file_content,
            filename=file.name
        )
        
        if "error" in result:
            await cl.Message(content=f"❌ Error: {result['error']}").send()
        else:
            await cl.Message(content=f"✅ `{file.name}` guardado correctamente en la base de datos.").send()


@cl.on_message
async def on_message(message: cl.Message):
    
    r = Requests()
    
    msg = cl.Message(content="🔍 Analizando tu pregunta...")
    await msg.send()
    
    ##Llamar al endpoint RAG con validación
    result = r.request_rag(question=message.content)
    
    if "error" in result:
        msg.content = f"❌ Error: {result['error']}"
    else:
        # Construir respuesta con metadata
        response_text = result.get("generation", "Sin respuesta")
        
        # Agregar indicador si se refinó la query
        if result.get("refinement_attempts", 0) > 0:
            response_text += f"\n\n*ℹ️ Se refinó la búsqueda {result['refinement_attempts']} vez(ces) para obtener mejor contexto*"
        
        msg.content = response_text
    
    await msg.update()