from langchain.document_loaders import TextLoader
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.text_splitter import CharacterTextSplitter
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Step 1: Load the conversation
loader = TextLoader("conversation.txt")
docs = loader.load()

# Step 2: Split text into chunks
text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
split_docs = text_splitter.split_documents(docs)

# Step 3: Embed and index
embedding = OpenAIEmbeddings()
db = FAISS.from_documents(split_docs, embedding)

# Step 4: Create retriever and QA chain
retriever = db.as_retriever()
qa_chain = RetrievalQA.from_chain_type(llm=ChatOpenAI(model_name="gpt-4"), retriever=retriever)

query = "What were the main challenges I discussed in april?"
result = qa_chain.run(query)

print(result)
