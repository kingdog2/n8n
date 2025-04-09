##紀錄LLM對話 透過不同memory方法來處理同樣的memory。 下次對話時丟到LLM
import langchain
print(langchain.__version__)
from langchain_ollama import OllamaLLM
from langchain.agents import initialize_agent, AgentType, load_tools, Tool
import os
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from get_stock import get_stock_price#, search_stock_symbol
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationSummaryMemory, ConversationBufferWindowMemory
from langchain.chains import LLMChain
from langchain.schema import AIMessage, HumanMessage, SystemMessage

os.environ["SERPAPI_API_KEY"] =  your_key

ollama_model = OllamaLLM(model= "gemma3:4b")#deepseek-r1:latest")#"llama3.2:latest")
#, temperature=0 隨機設為0
print(ollama_model)


##LLM conversation_history紀錄歷史對話 一次丟進去
# template = """You are a chatbot having a conversation with a human.

# {conversation_history}

# Human: {input}
# Chatbot:"""

template = """You are a highly knowledgeable and wise teacher, capable of answering any question with great clarity and insight.

{conversation_history}

Human : {input}
Teacher :"""

prompt = PromptTemplate(
    input_variables=["conversation_history", "input"], template=template
)


##對話紀錄做摘要 推薦這長聊天
memory = ConversationSummaryMemory(llm=ollama_model,
                                   memory_key="conversation_history",  # 存储对话历史的键
                                   return_messages=True  # 返回详细的消息历史
                                   )

# memory = ConversationBufferWindowMemory(k=2, ##最多存放幾筆對話
                                        # memory_key="conversation_history",  # 存储内存的键
                                        # max_token_limit=300,               # 限制總共Token大小，避免太大
                                        # )
llm_chain = LLMChain(
    llm=ollama_model,
    prompt=prompt,
    verbose=True,
    memory=memory,
)
while 1:
    print(memory.chat_memory.messages)##各種memory將這些做不同處理，所以print時是一樣的
    result = llm_chain.invoke( 
        input("請輸入要問的問題:")
            # HumanMessage(content=) ##User提問
        )
    print(result)
    print('-'*50)
    print(result['text'])
    
    print("="*100)


##https://ithelp.ithome.com.tw/articles/10339290
# 1. ConversationBufferMemory
# 這種 Memory 允許存儲訊息，並將這些對話紀錄存到一個變數中。它的主要功能是將對話紀錄保存，並隨時提取。

# 2. ConversationBufferWindowMemory 最後 K 次
# 這種 Memory 保持對話中的交互作用列表。它只使用最後 K 次的互動。此種 Memory 可幫助系統追蹤到最近的參數 K 次交互作用，確保不會遺失重要的互動資訊。例如說 ConversationBufferWindowMemory(k=1)，就只會紀錄上一組對話。

# 3. ConversationTokenBufferMemory token 長度llm=llm, max_token_limit=50
# 這種 Memory 保有最近互動的暫存，並使用 token 長度而非互動的數量。它的主要功能是基於 token 的長度來儲存和管理互動，確保 Memory 使用的最大效率。這裡常見的有兩個參數，llm=llm, max_token_limit=50。llm 就是放入 ChatGPT 這種 AI model ，而 max_token_limit 是限制最多記得多長的 token 的對話紀錄。

# 4. ConversationSummaryMemory
# 這種 Memory 會把前面的對話紀錄做摘要。雖然看起來很不錯，但也是還要再放了一個參數是 llm，就由這個 LLM 來把對話紀錄做摘要。也就是說會比較消耗 ChatGPT token 量。

