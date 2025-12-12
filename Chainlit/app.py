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
                """Eres un asistente/profesor útil y conciso que ayuda a los usuarios a estudiar usando **únicamente** el PDF previamente subido como contexto.  
    - Usa exclusivamente la información presente en `{context}`.  
    - **No inventes** información. Si la respuesta no puede responderse con lo provisto, responde exactamente: "No puedo responder eso con la información provista." y, si es posible, sugiere 1–2 acciones para obtener la respuesta (por ejemplo: "Revisar la sección X del PDF" o "Subir más documentos").  
    - **No reveles razonamiento interno** (no escribir chain-of-thought). En lugar de eso, entrega:  
    1) **Respuesta** — respuesta clara y directa (1–3 frases);  
    2) **Justificacion en base al texto** — hasta 3 bullets que indiquen qué partes del `{context}` sustentan la respuesta;  
    """
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