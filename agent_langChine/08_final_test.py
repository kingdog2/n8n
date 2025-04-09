#QA chain，结合 Chroma 来实现PDF文档的语义化搜索
# pip install pymupdf
PDF_NAME = r'C:\Users\f2201\Downloads\nvidia.pdf'

##分割
from langchain.document_loaders import PyMuPDFLoader
docs = PyMuPDFLoader(PDF_NAME).load()
print (f'There are {len(docs)} document(s) in {PDF_NAME}.')
print (f'There are {len(docs[0].page_content)} characters in the first page of your document.')

print('-'*100)
##變成向量
from langchain.embeddings.ollama import OllamaEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
split_docs = text_splitter.split_documents(docs)

embeddings = OllamaEmbeddings(model= "llama3.2:latest")

vectorstore = Chroma.from_documents(split_docs, embeddings, collection_name="serverless_guide")
print('-'*100)


from langchain.llms import OpenAI
from langchain.chains.question_answering import load_qa_chain

llm = OpenAI(temperature=0)
chain = load_qa_chain(llm, chain_type="stuff")
print('-'*100)
query = "What is the use case of AWS Serverless?"
similar_docs = vectorstore.similarity_search(query, 3, include_metadata=True)
print('-'*100)
chain.run(input_documents=similar_docs, question=query)