##Agent與工具
from langchain_ollama import OllamaLLM
from langchain.agents import initialize_agent, AgentType, load_tools, Tool
import os
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
# from get_stock import get_stock_price#, search_stock_symbol
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationSummaryMemory

from langchain.agents import get_all_tool_names
print(get_all_tool_names())


os.environ["SERPAPI_API_KEY"] =  "f20653ede959a30dd3abe20f53d37cb7767b541b0957de3ae3c7c2daeb513586"

ollama_model = OllamaLLM(model= "gemma3:4b")

print(ollama_model)

tools = load_tools(["serpapi", "llm-math"], llm=ollama_model)
# tools.append(
#     Tool(
#         name="股票的價格",
#         func=get_stock_price,
#         description="獲取股票價格，並输出数据出來。請注意輸入格式為 股票名稱, 過去天數(不要'天'這個字) ex:AAPL, 30。代表APPL前30天股價"
#     )
# )
print(len(tools))

agents = initialize_agent(tools, ollama_model, agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True , max_iterations=8)#, handle_parsing_errors=True)
response = agents.run("台灣101大樓和自由女神高度相差多少")
print("="*100)
print(response)



# Zero-shot ReAct
# 利用 ReAct 框架根据工具的描述来决定使用哪个工具，可以使用多个工具，但需要为每个工具提供描述信息。工具的选择单纯依靠工具的描述信息。关于 ReAct 框架的更多信息，请参考 ReAct。
# Structured Input ReAct
# 相较于单一字符串作为输入的代理，该类型的代理可以通过工具的参数schema创建结构化的动作输入。
# OpenAI Functions
# 该类型的代理用来与OpenAI Function Call机制配合工作。
# Conversational
# 这类代理专为对话场景设计，使用具有对话性的提示词，利用 ReAct 框架选择工具，并利用记忆功能来保存对话历史。
# Self ask with search
# 这类代理利用工具查找问题的事实性答案。
# ReAct document store
# 利用 ReAct 框架与文档存储进行交互，使用时需要提供 Search 工具和 Lookup 工具，分别用于搜索文档和在最近找到的文档中查找术语。
# Plan-and-execute agents
# 代理规划要做的事情，然后执行子任务来达到目标。