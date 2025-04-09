##有收尋、查股票價格、記憶 功能
#pip install langchain langchain-community langchain-ollama google-search-results
import langchain
print(langchain.__version__)
from langchain_ollama import OllamaLLM
from langchain.agents import initialize_agent, AgentType, load_tools, Tool
import os
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from get_stock import get_stock_price#, search_stock_symbol
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationSummaryMemory
from langchain.agents import get_all_tool_names
print(get_all_tool_names())

# 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

#private解密
def open_private_key():
    with open(r'C:\Users\f2201\Downloads\agent_langChine\private_key.pem', 'rb') as private_file:
        key = RSA.import_key(private_file.read())
        print(key)
    return key

print(open_private_key)
def decrypt_message(private_key, encrypted_message):
    cipher = PKCS1_OAEP.new(private_key)
    decrypted_message = cipher.decrypt(encrypted_message)
    return decrypted_message.decode()

if __name__ == "__main__":
    try:
        ##先RSA解密Serp Api Key
        with open(r'C:\Users\f2201\Downloads\agent_langChine\encrypted_message.txt', 'rb') as file:
            message = file.read()
        use_private_key = open_private_key()
        os.environ["OPENAI_API_KEY"] = "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"
        os.environ["SERPAPI_API_KEY"] =  decrypt_message(use_private_key, message)
        #"f20653ede959a30dd3abe20f53d37cb7767b541b0957de3ae3c7c2daeb513586"
        print(os.environ["SERPAPI_API_KEY"])
        
        ##LLM
        template = """You are a chatbot having a conversation with a human.

            {conversation_history}
            
            Human: {input}
            Chatbot:"""
            
        prompt = PromptTemplate(
            input_variables=["conversation_history", "input"], template=template
        )
        
        print("="*100)
        ollama_model = OllamaLLM(model= "gemma3:4b")#deepseek-r1:latest")#"llama3.2:latest")
        memory = ConversationSummaryMemory(
                llm=ollama_model,
                memory_key="conversation_history",  # 存储内存的键
                # max_token_limit=1000,               # 限制内存大小，避免过大
                # return_messages=True                # 是否返回所有消息作为总结
            )
        print(ollama_model)
        
        
        # response = ollama_model.invoke("今天台灣新聞")
        # print(f"Generated Text: {response}")
        tools = load_tools(["serpapi"], llm=ollama_model, description="提供的搜索功能来查找最新的資料")
        tools.extend(load_tools(["dalle-image-generator"]))
        tools.append(
            Tool(
                name="股票的價格",
                func=get_stock_price,
                description="獲取股票價格，並输出数据出來。請注意輸入格式為 股票名稱, 過去天數(不要'天'這個字) ex:AAPL, 30。代表APPL前30天股價"
            )
        )
        print(len(tools))
 
        agents = initialize_agent(tools, ollama_model, memory=memory, prompt=prompt, agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True , max_iterations=8)#, handle_parsing_errors=True)
        response = agents.invoke("請直接給我 MSFT 過去 100 天的股票價格")
        print("="*100)
        print(response)
            
        while 1: #給我 MSFT 2025-03-19的股價
            print(memory.chat_memory.messages)
            response = agents.invoke(input("請輸入要問的問題:"))
            print("="*100)
            print(response)
    except Exception as e:
        print(f"錯誤: {e}")
        
        
# 特性	SELF_ASK_WITH_SEARCH	ZERO_SHOT_REACT_DESCRIPTION
# 自我提问	会提问自己，确认是否需要搜索	不会提问，直接进行任务处理