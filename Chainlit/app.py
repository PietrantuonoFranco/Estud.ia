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
    
    ##Instancia del modelo
    model = init_chat_model("google_genai:gemini-2.5-flash-lite")
    
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
    
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "Tu eres un asistente útil que ayuda a los usuarios respondiendo sus preguntas basándote en el pdf que se subió previamente. "
                "Utiliza el contexto proporcionado para responder de la mejor manera posible. Si no sabes la respuesta, di que no lo sabes.\n\n"
                "El contexto con el que debes formular la respuesta es el siguiente:\n{context}"
            ),
            ("human", "{question}"),
        ]
    )
    runnable = prompt | model | StrOutputParser() ##Creamos el pipeline al iniciar el chat
    cl.user_session.set("runnable", runnable)


@cl.on_message
async def on_message(message: cl.Message):
    
    r = Requests()
    
    runnable = cast(Runnable, cl.user_session.get("runnable"))  # type: Runnable

    msg = cl.Message(content="")

    async for chunk in runnable.astream(
        {"question": message.content, "context": r.request_get_context(query=message.content, filter="")},
        config=RunnableConfig(callbacks=[cl.LangchainCallbackHandler()]),
    ):
        await msg.stream_token(chunk)

    await msg.send()