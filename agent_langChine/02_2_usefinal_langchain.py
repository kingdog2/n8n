##使用知識庫  **Chroma有錯誤
from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.ollama import OllamaEmbeddings
from langchain.vectorstores import Chroma
import os
os.environ["CUDA_VISIBLE_DEVICES"] = "1"
with open(r"C:\Users\f2201\OneDrive\桌面\本地Ollama.txt", "r", encoding="utf-8") as f:
    text = f.read()

with open("elon_musk_utf8.txt", "w", encoding="utf-8") as f:
    f.write(text) 

loader = TextLoader("elon_musk_utf8.txt" , encoding = 'UTF-8')
docs = loader.load()

print(docs)

# ollama_model = OllamaLLM(model= "gemma3:4b")
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
documents = text_splitter.split_documents(docs)
db = Chroma.from_documents(documents, OllamaEmbeddings(model= "llama3.2:latest"))
print("\n654444444444444\n")
##歐肌理得距離
query = "誰是賴依清德"
docs = db.similarity_search(query)
print(docs[0].page_content)