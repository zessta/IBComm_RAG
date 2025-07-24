import hashlib
import pickle
import logging
import time
from pathlib import Path
from typing import Optional
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from IBComm_RAG_api.globals import embedding_model

logger = logging.getLogger(__name__)


class VectorDBSingleton:
    """
    A singleton class for managing FAISS vector stores per document and group.
    Ensures each (document_path, group_id) pair has only one instance.
    Updates the vector store only when the source document changes.
    """

    _instances = {}

    def __new__(cls, document_path: str, group_id: str):
        """
        Returns a singleton instance for a given (document_path, group_id) pair.
        """
        key = (document_path, group_id)
        if key not in cls._instances:
            cls._instances[key] = super(VectorDBSingleton, cls).__new__(cls)
        return cls._instances[key]

    def __init__(self, document_path: str, group_id: str):
        """
        Initializes the VectorDBSingleton with paths and metadata files.
        
        Args:
            document_path (str): Path to the input document.
            group_id (str): Unique group identifier for namespacing the vector store.
        """
        self.document_path = document_path
        self.group_id = group_id
        self.vectorstore_dir = Path(f"/home/Praveen_ZT/IBComm_RAG_api/vector_stores/{group_id}")
        self.vectorstore_file = self.vectorstore_dir / "index.faiss"
        self.metadata_file = self.vectorstore_dir / "metadata.pkl"
        self.vs: Optional[FAISS] = None

        self._ensure_directory()

    def _ensure_directory(self):
        """
        Ensures that the vectorstore directory exists.
        """
        self.vectorstore_dir.mkdir(parents=True, exist_ok=True)

    def _compute_checksum(self) -> str:
        """
        Computes the SHA256 checksum of the source document.
        
        Returns:
            str: The computed checksum.
        """
        sha256 = hashlib.sha256()
        with open(self.document_path, "rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                sha256.update(chunk)
        return sha256.hexdigest()

    def _load_metadata(self):
        """
        Loads metadata from disk, if available.

        Returns:
            dict: Metadata dictionary containing checksum or other values.
        """
        if self.metadata_file.exists():
            with open(self.metadata_file, "rb") as f:
                return pickle.load(f)
        return {}

    def _save_metadata(self, metadata):
        """
        Saves metadata to disk.

        Args:
            metadata (dict): Dictionary to store metadata (e.g., checksum).
        """
        with open(self.metadata_file, "wb") as f:
            pickle.dump(metadata, f)

    def _generate_vectorstore(self):
        """
        Generates a FAISS vector store from the document and saves it to disk.
        Also stores the computed checksum in metadata.
        """
        logger.info("Generating vectorstore from scratch...")

        start = time.time()
        loader = TextLoader(self.document_path)
        docs = loader.load()

        splitter = RecursiveCharacterTextSplitter(chunk_size=400, chunk_overlap=60)
        splits = splitter.split_documents(docs)

        self.vs = FAISS.from_documents(splits, embedding_model)
        self.vs.save_local(str(self.vectorstore_dir))

        checksum = self._compute_checksum()
        self._save_metadata({"checksum": checksum})

        logger.info(f"Vectorstore created and saved in {time.time() - start:.2f} seconds.")

    def update_vectorstore_if_needed(self) -> bool:
        """
        Updates the vectorstore only if the document content has changed.

        Returns:
            bool: True if the vector store was regenerated, False otherwise.
        """
        current_checksum = self._compute_checksum()
        metadata = self._load_metadata()
        old_checksum = metadata.get("checksum")

        if current_checksum != old_checksum or not self.vectorstore_file.exists():
            logger.info("Document has changed or FAISS index missing. Regenerating vectorstore...")
            self._generate_vectorstore()
            return True
        else:
            logger.debug("No changes in document. Vectorstore update skipped.")
            return False

    def get_vectorstore(self) -> FAISS:
        """
        Loads and returns the FAISS vector store instance.

        Returns:
            FAISS: The FAISS vector store object.
        """
        if self.vs is not None:
            logger.debug("Returning already loaded vectorstore.")
            return self.vs

        try:
            logger.info("Loading vectorstore from disk...")
            start = time.time()
            self.vs = FAISS.load_local(
                str(self.vectorstore_dir),
                embedding_model,
                allow_dangerous_deserialization=True
            )
            logger.info(f"Vectorstore loaded in {time.time() - start:.2f} seconds.")
        except Exception as e:
            logger.error(f"Failed to load vectorstore: {e}")
            raise e

        return self.vs
