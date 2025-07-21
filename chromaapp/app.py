from fastapi import FastAPI, Request
from pydantic import BaseModel
from vector_store import VectorDBSingleton
from llm_call import chat_with_model
app = FastAPI()
singleton = VectorDBSingleton()

class QueryRequest(BaseModel):
    text: str

@app.post("/update")
def update_vector_db():
    updated = singleton.update_vectorstore_if_needed()
    return {"status": "updated" if updated else "no_change"}

# FastAPI Endpoint
@app.post("/query")
def query_vector_db(request: QueryRequest):
    question = request.text
    vs = singleton.get_vectorstore()
    retriever = vs.as_retriever(search_kwargs={"k": 3})
    docs = retriever.get_relevant_documents(question)
    results = [doc.page_content for doc in docs]
    response = chat_with_model(text=results, query=question)
    return {"results": response}
