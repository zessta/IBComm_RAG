import logging
from IBComm_RAG_api.globals import embedding_model

logger = logging.getLogger(__name__)

def load_embedding_model():
    logger.info("Loading embedding model...")
    _ = embedding_model
    logger.info("Embedding model loaded successfully.")