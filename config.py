# config.py
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.llms import Ollama

def get_llm():
    return Ollama(
        model="llama3.2",
        callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]),
        base_url="http://localhost:11434",
        temperature=0.7
    )