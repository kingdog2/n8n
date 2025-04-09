###############處理Model的輸出
##資料改變格式
from langchain.output_parsers import CommaSeparatedListOutputParser
output_parser = CommaSeparatedListOutputParser()
print(output_parser.parse("ABC, FFF, JIJLJO, JIfjoWDK:;am"))


##格式化指令
from langchain.output_parsers import StructuredOutputParser, ResponseSchema
from langchain.prompts import PromptTemplate, ChatPromptTemplate, HumanMessagePromptTemplate
from langchain_ollama import OllamaLLM

##定義回答的結構
response_schemas = [
        ResponseSchema(name="answer", description="answer to the user's question"),
        ResponseSchema(name="source", description="source referred to answer the user's question, should be a website.")
    ]

#創建一個解析器，將模型的輸出->結構化的JSON格式
output_parser = StructuredOutputParser.from_response_schemas(response_schemas)

# 告訴Model如何返回結果的結構
format_instructions = output_parser.get_format_instructions()

# partial_variables允许在代码中预填充提示此模版的部分变量。这类似于接口，抽象类之间的关系
prompt = PromptTemplate(
    template="answer the users question as best as possible.\n{format_instructions}\n{question}",
    input_variables=["question"], ## 輸入變量：問題格式
    partial_variables={"format_instructions": format_instructions} ##回答格式
)

ollama_model = OllamaLLM(model= "gemma3:4b", temperature=0)


response = prompt.format_prompt(question="what's the capital of France?")
output = ollama_model.invoke(response.to_string())
print(output)
####格式化的輸出
output_parser.parse(output)