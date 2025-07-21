import hashlib
from typing import List
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_core.documents import Document
from const import *


class VectorDBSingleton:
    """
    Singleton class that manages a Chroma vector database backed by HuggingFace embeddings.
    It watches for changes in the document file and updates the vector store only if the file changes.
    """
    _instance = None


    def __new__(cls):
        """
        Implements the singleton pattern. Instantiates the class only once.
        """

        if cls._instance is None:
            print("[INFO] Initializing VectorDB Singleton")
            cls._instance = super().__new__(cls)
            cls._instance.embedding = HuggingFaceEmbeddings(model_name=HF_MODEL_NAME)
            cls._instance.vectorstore = None
            cls._instance.last_hash = None
        return cls._instance



    def compute_file_hash(self, file_path: str) -> str:
        """
        Computes an MD5 hash of the given file to detect content changes.

        Args:
            file_path (str): Path to the document file.

        Returns:
            str: MD5 hash string of the file content.
        """

        with open(file_path, "rb") as f:
            return hashlib.md5(f.read()).hexdigest()



    def load_documents(self) -> List[Document]:
        """
        Loads and splits the document into smaller chunks for vectorization.

        Returns:
            List[Document]: A list of document chunks.
        """

        loader = TextLoader(DOCUMENT_PATH)
        documents = loader.load()
        text_splitter = CharacterTextSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)
        return text_splitter.split_documents(documents)



    def update_vectorstore_if_needed(self):
        """
        Updates the vector store only if the underlying document content has changed.

        Returns:
            bool: True if an update was made, False if no update was needed.
        """

        current_hash = self.compute_file_hash(DOCUMENT_PATH)
        if self.last_hash == current_hash and self.vectorstore:
            return False  # No update needed
        print("[INFO] Updating vector store...")
        documents = self.load_documents()
        self.vectorstore = Chroma.from_documents(
            documents, self.embedding, persist_directory=CHROMA_DB_DIR
        )
        self.vectorstore.persist()
        self.last_hash = current_hash
        return True



    def get_vectorstore(self):
        """
        Returns the current Chroma vector store. Loads it from disk if not already in memory.

        Returns:
            Chroma: The Chroma vector store instance.
        """

        if self.vectorstore is None:
            print("[INFO] Loading vector store from disk...")
            self.vectorstore = Chroma(persist_directory=CHROMA_DB_DIR, embedding_function=self.embedding)
        return self.vectorstore
