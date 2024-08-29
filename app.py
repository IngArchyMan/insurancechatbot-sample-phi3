from langchain_community.llms import Ollama
from langchain.prompts import ChatPromptTemplate
import chainlit as chat

CHAIN_VARIABLE_SESSION = "chain"

# Cambiar a un modelo confirmado y disponible
model = Ollama(
    model="Phi3:mini" # Asegúrate de que este modelo esté disponible
)

@chat.on_chat_start
async def on_chat_start():
    await chat.Message(content="Welcome to the InsuranceBot").send()
    
    # Usar un modelo confirmado
    llm = Ollama(model="Phi3:mini")  # Asegúrate de que "mistral" esté disponible en Ollama
    
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "You are an insurance agent"),
            ("user", "{question}"),
        ])
    
    chain = prompt | llm 
    
    chat.user_session.set(CHAIN_VARIABLE_SESSION, chain)
    
@chat.on_message
async def on_message(message):
    user_message = message.content
    chain = chat.user_session.get(CHAIN_VARIABLE_SESSION)
    
    message = chat.Message(content="")
    
    async for chunk in chain.astream({
        "question": user_message
    }):
        await message.stream_token(chunk)
    
    await message.send()
    
@chat.on_chat_end
async def on_chat_end():
    await chat.Message(content="Goodbye!").send()
