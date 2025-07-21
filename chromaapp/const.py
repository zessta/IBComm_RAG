# ========================
# Configuration Constants
# ========================

# Name of the HuggingFace embedding model used for vectorization
HF_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

# Path to the input text file containing the source conversation or document
DOCUMENT_PATH = "conversation.txt"

# Directory path where the Chroma vector database will be stored/persisted
CHROMA_DB_DIR = "./chroma_db"

# Number of characters in each text chunk for embedding
CHUNK_SIZE = 200

# Number of overlapping characters between chunks (to preserve context)
CHUNK_OVERLAP = 20