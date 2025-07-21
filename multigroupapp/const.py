# ========================
# Configuration Constants
# ========================

# Name of the HuggingFace embedding model used for vectorization
HF_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

# Number of characters in each text chunk for embedding
CHUNK_SIZE = 400

# Number of overlapping characters between chunks (to preserve context)
CHUNK_OVERLAP = 60
