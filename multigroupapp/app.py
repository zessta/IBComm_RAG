from fastapi import FastAPI, HTTPException
import traceback, logging
from llama_call import chat_with_model
from vector_store import VectorDBSingleton
from models.models import UpdateVectorRequest, QueryRequest
from globals import embedding_model  
app = FastAPI()

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Ensure embeddings are initialized only once on server startup
@app.on_event("startup")
def startup_event():
    logger.info("Loading embedding model...")
    _ = embedding_model  # Force loading at startup
    logger.info("Embedding model loaded successfully.")


@app.post("/update_vectorstore")
def update_vectorstore(request: UpdateVectorRequest):
    """
    Updates vector store for a specific group_id and document_path.
    Call this periodically (e.g., every 10 min from a daemon).
    """
    try:
        logger.info(f"Checking for updates for group_id={request.group_id}, path={request.document_path}")
        singleton = VectorDBSingleton(document_path=request.document_path, group_id=request.group_id)
        updated = singleton.update_vectorstore_if_needed()

        return {
            "group_id": request.group_id,
            "document_path": request.document_path,
            "updated": updated,
            "message": "Vector store updated" if updated else "No changes detected"
        }

    except ValueError as ve:
        logger.error(f"Validation error: {ve}")
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        logger.error(f"Unhandled error: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail="Internal server error")



@app.post("/query")
def query_vector_db(req: QueryRequest):
    """
    Query vector DB for a given group and document.
    If the file is changed, it will refresh the vector store first.
    """
    try:
        logger.info(f"Received query request for group_id='{req.group_id}', doc='{req.document_path}'")
        singleton = VectorDBSingleton(document_path=req.document_path, group_id=req.group_id)

        # Auto-refresh if changes detected
        updated = singleton.update_vectorstore_if_needed()
        if updated:
            logger.info(f"Vector store updated for group_id='{req.group_id}'")

        # Query vector store
        vs = singleton.get_vectorstore()
        retriever = vs.as_retriever(search_kwargs={"k": 3})
        docs = retriever.get_relevant_documents(req.text)

        if not docs:
            raise HTTPException(status_code=404, detail="No relevant documents found.")

        results = [doc.page_content for doc in docs]
        response = chat_with_model(text=results, query=req.text)

        return {
            "group_id": req.group_id,
            "document_path": req.document_path,
            "response": response,
            "retrieved_docs": results
        }

    except ValueError as ve:
        logger.error(f"Validation error: {ve}")
        raise HTTPException(status_code=400, detail=str(ve))
    except FileNotFoundError as fe:
        logger.error(f"File not found: {fe}")
        raise HTTPException(status_code=404, detail=str(fe))
    except Exception as e:
        logger.error("Unhandled exception occurred:")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail="Internal server error")
