# IBComm_RAG
This script builds a local question-answering (QA) system over a .txt conversation file By retrieve and generate answers from the data.


# Conversation QA System (RAG with FAISS)

This is a simple Retrieval-Augmented Generation (RAG) demo built using:

- **LangChain**
- **HuggingFace Embeddings**
- **FAISS** (Vector DB)
- **TextLoader** for document ingestion

It loads a plain text file, splits it into overlapping chunks, embeds the chunks using a sentence-transformer model, builds a FAISS vector index, and then allows querying the document for relevant information.


##  Quick Start

### 1. Install Dependencies

```bash
pip install langchain langchain-community faiss-cpu sentence-transformers
```

Note: If you're using a GPU or want better performance, you may use faiss-gpu instead.

2. Add Your Document
Place a plain text file in the root directory named check.txt.
This file should contain your source content (e.g., a monthly report or data logs).


⚙️ Configuration
- You can change the following variables in the script:

```bash
Variable :	Purpose
DOCUMENT_PATH:	Path to the input text document
CHUNK_SIZE:	Number of characters per chunk
CHUNK_OVERLAP:	Number of characters to overlap between chunks
HF_MODEL_NAME:	Name of HuggingFace embedding model (e.g., MiniLM-L6-v2)
```

## Example Use Case
This setup is ideal for:

- Querying monthly/Yearly reports (e.g., "How many visitors in July?")

- Extracting specific facts from long plain-text logs

- Lightweight document-based QA without LLM

## 🔍 Sample Model
By default, it uses:

- sentence-transformers/all-MiniLM-L6-v2
#### You can change this in the code for higher-accuracy models like:

- all-mpnet-base-v2

- multi-qa-MiniLM-L6-cos-v1