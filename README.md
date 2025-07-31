
# IBComm RAG API

A FastAPI-based backend service that powers Group Messaging and Retrieval-Augmented Generation (RAG) using vector embeddings. This system allows saving user messages, querying documents, updating vector stores, and managing group-level data.

---

## Project Structure

```

IBComm_RAG/
├── api/                   # Route handlers (delete, query, save, update)
├── core/                  # Startup logic (e.g., loading embedding models)
├── group_texts/          # Group-level raw or processed text data (optional)
├── models/                # Pydantic request/response models
├── services/              # Business logic
├── utils/                 # Utility functions and helpers
├── vector_stores/         # Vector DB (Dynamically we will create)
├── app.py                 # Main FastAPI app entry
├── const.py               # Constants used across the app
├── globals.py             # Global config or variables
├── requirements.txt       # Python dependencies
└── .gitignore             # Git ignore rules

````

---

## Features

-  Group Message Ingestion
-  Document Embedding & Querying
-  Vector Store Update
- Built-in Swagger & ReDoc API documentation

---

## Installation

1. **Clone the repository**

```bash
git clone https://github.com/zessta/IBComm_RAG.git
cd IBComm_RAG
````

2. **Create and activate a virtual environment (optional but recommended)**

```bash
python3 -m venv venv
source venv/bin/activate 
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

---

## Running the Server

### Option 1: Normal Run

```bash
uvicorn app:IBComm_RAG --reload --host 0.0.0.0 --port 5000
```


---

## API Documentation

* Swagger UI: [http://74.225.221.182:5000/v1/docs](http://74.225.221.182:5000/v1/docs)
* ReDoc UI: [http://74.225.221.182:5000//v1/redoc](http://74.225.221.182:5000//v1/redoc)

---

## Key Endpoints

| Method | Endpoint Prefix        | Purpose                          | Tag             |
| ------ | ---------------------- | -------------------------------- | --------------- |
| POST   | `/save_message/`       | Save messages to a group         | Group Messaging |
| POST   | `/update_vectorstore/` | Update document vector store     | Vector Store    |
| POST   | `/query/`              | Query documents using embeddings | Query           |
| DELETE | `/delete_group/`       | Delete group data                | Group Delete    |

---

##  Embedding Model Initialization

The model is loaded during FastAPI app startup:

```python
@IBComm_RAG.on_event("startup")
def startup_event():
    load_embedding_model()
```

Defined in `core/startup.py`.

---

##  Tech Stack

* [FastAPI](https://fastapi.tiangolo.com/)
* [Uvicorn](https://www.uvicorn.org/)
* Python 3.8+

---


