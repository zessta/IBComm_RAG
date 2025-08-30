# Multi-Group RAG API
This is a FastAPI-based backend service that supports multi-group text message saving, vector store creation, and question-answering over group-specific documents using RAG (Retrieval-Augmented Generation).

## Features
- Save messages per group_id into separate text files.
- Periodically update vector stores for each group (FAISS or similar backend).
- Handle semantic search queries with retrieval from group-specific documents.
- Integrate with a local or hosted LLM using the chat_with_model function.

Embedding model loaded once on startup to optimize performance.

📁 Directory Structure
```bash
IBComm_RAG/
├── multigroupapp/
│   ├── app.py                  # FastAPI main app
│   ├── llama_call.py           # LLM query handler
│   ├── vector_store.py         # Singleton for managing vector DB per group
│   ├── getPath.py              # Utility to fetch path for group_id
│   ├── models/
│   │   └── models.py           # Pydantic request models
│   └── group_texts/            # Stores .txt files for each group
```
##  API Endpoints
### POST /save_message
Save a message under a specific group_id.

Request:

```json
{
  "group_id": "group123",
  "message": "Hello world!",
  "timestamp": "2025-07-22T12:00:00Z" // optional
}
```
Response:

```json
{ "status": "success" }
```

### POST /update_vectorstore
Update the vector store for a group's document.

Request:

```json
{
  "group_id": "group123",
  "document_path": "/path/to/group123.txt"
}
```

Response:
```json
{
  "group_id": "group123",
  "document_path": "...",
  "updated": true,
  "message": "Vector store updated"
}
```
### POST /query
- Query the vector store for a relevant answer based on prior messages.

Request:
```json
{
  "group_id": "group123",
  "text": "What did we discuss about onboarding?"
}
```
Response:

```json
{
  "group_id": "group123",
  "document_path": "...",
  "response": "Here's a summary based on retrieved docs...",
  "retrieved_docs": [
    "... relevant content 1 ...",
    "... relevant content 2 ..."
  ]
}
```
## Setup Instructions
1. Install dependencies
```bash
pip install -r requirements.txt
```

- Make sure you also have necessary dependencies for LLM integration, vector DB (e.g., faiss-cpu, langchain, etc.).

2. Set environment variable
```bash
export GROUP_TEXT_DIR=/path/to/group_texts
```

Or let it default to /home/azureuser/IBComm_RAG/multigroupapp/group_texts.

3. Run the server
```bash
uvicorn app:app --host 0.0.0.0 --port 8000
```

### Components
- LLM: Controlled via chat_with_model() in llama_call.py.
- Vector Store: Managed with singleton class in vector_store.py.
- Embeddings: Loaded once on startup using embedding_model from globals.py.

