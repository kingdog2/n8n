##知識庫 讀取>>分割>>向量化分割塊>>使用
from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter, RecursiveCharacterTextSplitter, MarkdownHeaderTextSplitter, Language
import os

##########讀取文件
# 讀取變成UTF-8
with open(r"C:\Users\f2201\OneDrive\桌面\本地Ollama.txt", "r", encoding="utf-8") as f:
    text = f.read()

with open("elon_musk_utf8.txt", "w", encoding="utf-8") as f:
    f.write(text) 

loader = TextLoader("elon_musk_utf8.txt" , encoding = 'UTF-8')
docs = loader.load()

print(docs)

print("\n!!!!!!!!!!  第一階段讀取文件完成!!\n")

##########-----分割文件
text_splitter = CharacterTextSplitter(
        separator= "\n\n", ##用這個當分隔符號
        chunk_size= 1000,
        chunk_overlap= 200,
        length_function= len,
    )
split_docs = text_splitter.split_documents(docs)
print(split_docs)
print('='*100)

##自-----訂分割
text_splitter = RecursiveCharacterTextSplitter(
        chunk_size= 1000,
        chunk_overlap= 200,
        length_function= len,
    )
text = text_splitter.split_documents(docs)
print(text)
print('='*100)

##-----程式碼
PYTHONE_CODE = """
def Hello_print():
    print("你好!!")
####印出你好!!
Hello_print()
"""
python_splitter = RecursiveCharacterTextSplitter.from_language(
        language=Language.PYTHON, 
        chunk_size= 50,
        chunk_overlap= 0,
    )
python_docs = python_splitter.create_documents([PYTHONE_CODE])
print(python_docs)
print('='*100)

##-----MarkDown
markdown_document = "# Chapter 1\n\n    ## Section 1\n\nHi this is the 1st section\n\nWelcome\n\n ### Module 1 \n\n Hi this is the first module \n\n ## Section 2\n\n Hi this is the 2nd section"

headers_to_split_on = [
    ("#", "Header 1"),
    ("##", "Header 2"),
    ("###", "Header 3"),
]

splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)
splits = splitter.split_text(markdown_document)
print(splits)
print('='*100)


##-----用Token分割
text_splitter = CharacterTextSplitter.from_tiktoken_encoder(
    chunk_size=100, chunk_overlap=0
)
split_docs = text_splitter.split_documents(docs)
print(split_docs)
print('='*100)


print("\n!!!!!!!!!!  第二階段分割文件完成!!\n")

##########向量化分割塊 存進向量資料庫
# pip install chromadb onnxruntime==1.15.0
# pip install onnxruntime-gpu 
from langchain.embeddings.ollama import OllamaEmbeddings
from langchain.vectorstores import Chroma


# ollama_model = OllamaLLM(model= "gemma3:4b")
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
documents = text_splitter.split_documents(docs)
db = Chroma.from_documents(documents, OllamaEmbeddings(model= "llama3.2:latest"))

##歐肌理得距離
query = "誰是賴依清德"
docs = db.similarity_search(query)
print(docs[0].page_content)