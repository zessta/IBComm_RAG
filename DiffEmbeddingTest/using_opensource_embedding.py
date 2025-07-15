import os
import logging
from typing import List

from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain_core.documents import Document

DOCUMENT_PATH  = "check.txt"
CHUNK_SIZE     = 200
CHUNK_OVERLAP  = 20
HF_MODEL_NAME  = "sentence-transformers/all-MiniLM-L6-v2"  # change if you prefer a different model

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

def load_and_split_documents(path: str, chunk_size: int, overlap: int) -> List[Document]:
    if not os.path.exists(path):
        logger.error(f"File not found: {path}")
        raise FileNotFoundError(f"Document file '{path}' does not exist.")

    file_size = os.path.getsize(path)
    logger.info(f"File size: {file_size} bytes")
    if file_size == 0:
        raise ValueError("Document file is empty")

    loader = TextLoader(path, encoding='utf-8')
    docs   = loader.load()
    if not docs:
        raise ValueError("No content found in document")

    total_content   = docs[0].page_content
    content_length  = len(total_content)
    logger.info(f"Total content length: {content_length} characters")
    logger.info(f"First 200 characters: {repr(total_content[:200])}")

    # Adjust chunk size for very small files
    if content_length < chunk_size:
        chunk_size = max(100, content_length)
        overlap    = min(overlap, chunk_size // 4)

    text_splitter = CharacterTextSplitter(
        chunk_size     = chunk_size,
        chunk_overlap  = overlap,
        separator      = "\n",
        length_function= len
    )
    split_docs = text_splitter.split_documents(docs)

    if not split_docs:
        logger.warning("Text splitter produced no chunks, returning full content as single chunk.")
        return [Document(page_content=total_content)]

    for i, doc in enumerate(split_docs[:3]):
        logger.info(f"Chunk {i+1} length: {len(doc.page_content)}")
        logger.info(f"Chunk {i+1} preview: {repr(doc.page_content[:100])}")

    return split_docs

def create_vector_store(docs: List[Document], embedding: HuggingFaceEmbeddings) -> FAISS:
    if not docs:
        raise ValueError("No documents provided to create vector store")
    logger.info("Creating FAISS vector store...")
    return FAISS.from_documents(docs, embedding)

class SimpleRetrievalQA:
    def __init__(self, retriever, k: int = 3):
        self.retriever = retriever
        self.k         = k

    def run(self, query: str) -> str:
        try:
            logger.info(f"Running query: {query}")
            self.retriever.search_kwargs = {"k": self.k}
            docs = self.retriever.get_relevant_documents(query)
            if not docs:
                return "No relevant documents found."
            return "\n\n".join([f"Document {i+1}:\n{doc.page_content}" for i, doc in enumerate(docs)])
        except Exception as e:
            logger.error(f"Error during retrieval: {e}")
            return f"Error: {str(e)}"

def main():
    try:
        logger.info("Starting document QA system...")
        docs = load_and_split_documents(DOCUMENT_PATH, CHUNK_SIZE, CHUNK_OVERLAP)
        logger.info(f"Loaded and split {len(docs)} document chunks.")

        total_chars = sum(len(doc.page_content) for doc in docs)
        logger.info(f"Total characters across chunks: {total_chars}")
        logger.info(f"Average chunk size: {total_chars / len(docs):.1f}")

        # Instantiate HuggingFace embeddings
        embedding = HuggingFaceEmbeddings(model_name=HF_MODEL_NAME)

        # Build FAISS index
        db        = create_vector_store(docs, embedding)
        retriever = db.as_retriever()

        # Simple Retrieval QA
        qa     = SimpleRetrievalQA(retriever)
        query  = "What is the total people count in july month?"
        answer = qa.run(query)

        print("=" * 50)
        print("QUERY:", query)
        print("=" * 50)
        print("ANSWER:")
        print(answer)
        print("=" * 50)

    except FileNotFoundError as e:
        logger.error(e)
        print(f"Error: {e}")
    except Exception as e:
        logger.critical(f"Unhandled exception: {e}")
        print(f"Critical error: {e}")

if __name__ == "__main__":
    main()
