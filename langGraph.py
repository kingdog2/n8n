#State、Node、Edge、Graph
# pip install langgraph langchain langchain-ollama
# pip install langchain-openai
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph
from langgraph.graph.message import add_messages
from langchain_ollama import OllamaLLM
##記憶
from langgraph.checkpoint.memory import MemorySaver


##而memroy是下次重新跑graph能紀錄
##messages每次都會新增 方便graph其他能看node的return
class State(TypedDict):
    messages: Annotated[list, add_messages]


def chatbot(state: State):
    # 模板字符串
    template = """
    You are a chatbot having a conversation with a human.
    """
    

    print('*'*100)
    print([SystemMessage(content=template)] + state["messages"])
    print('*'*100)
    
    # 發送給LLM模型
    return {"messages": [AIMessage(llm.invoke([SystemMessage(content=template)] + state["messages"]))]}
    # return {"messages": [llm.invoke(state["messages"])]}

def chatbot2(state: State):
    print('@'*100)
    print(state["messages"])
    return {"messages": ["管理員中"]} 
llm = OllamaLLM(
    model="gemma3:4b",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)

graph_builder = StateGraph(State)
graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("chatbot2", chatbot2)
graph_builder.add_edge("chatbot", "chatbot2")
graph_builder.set_entry_point("chatbot") ##起點
graph_builder.set_finish_point("chatbot2") ##結束點





##記憶功能
config = {"configurable": {"thread_id": "chat1"}}
memory = MemorySaver()

##畫好編譯圖
graph = graph_builder.compile(checkpointer=memory) #checkpointer=memory

# 我的名子是陽藥
##開始
while True:
    user_input = input("使用者: ")
    if user_input.lower() in ["quit", "exit", "q"]:
        print("掰啦!")
        break
    input_message = HumanMessage(content=user_input)
    
    
    ##1.  直接打印結果，不要每個node都打印
    # output_result = graph.invoke({"messages": [input_message]}, config) #, config
    # print("\n直接打印結果\n")
    # print(output_result)
    
    print('-'*100)
    ##2.  stream values所有node結果  updates只傳node有更新的
    for event in graph.stream({"messages": [input_message]}, config, stream_mode="values"): #, config
        print('!'*100)
        print(event)
    #     # event["messages"][-1].pretty_print()
       
    print('-'*100)
    print('-'*100)