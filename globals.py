from langchain_community.embeddings import HuggingFaceEmbeddings
from IBComm_RAG_api.const import HF_MODEL_NAME
import logging

logger = logging.getLogger(__name__)

embedding_model = HuggingFaceEmbeddings(model_name=HF_MODEL_NAME)
logger.info("HuggingFace Embedding model loaded globally.")
