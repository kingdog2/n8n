##最基本
from langchain_ollama import OllamaLLM
from langchain.schema import AIMessage, HumanMessage, SystemMessage
import os
os.environ["SERPAPI_API_KEY"] =  

ollama_model = OllamaLLM(model= "gemma3:4b")#deepseek-r1:latest")#"llama3.2:latest")
#, temperature=0 隨機設為0
print(ollama_model)
result = ollama_model.invoke([
        SystemMessage(content="When people ask who are you? you must say 'I am 劉德華'."), ##系統
        HumanMessage(content="你是誰?") ##User提問
    ])
print(result)