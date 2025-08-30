from fastapi import FastAPI, HTTPException, Request
import traceback, logging, os, aiofiles,shutil
from llama_call import chat_with_model
from vector_store import VectorDBSingleton
from models.models import UpdateVectorRequest, QueryRequest, MessageRequest, DeleteRequest
from globals import embedding_model  
from pydantic import BaseModel
from datetime import datetime
from getPath import get_group_file_path

app = FastAPI(
    title="IBComm RAG API",
    description="API for saving group messages, updating vector stores, and querying documents using embeddings.",
    version="1.0.0",
    docs_url="/v1/docs",
    redoc_url="/v1/redoc"
)

DATA_DIR = os.getenv("GROUP_TEXT_DIR", "/home/Praveen_ZT/IBComm_RAG/multigroupapp/group_texts")
os.makedirs(DATA_DIR, exist_ok=True)


# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Ensure embeddings are initialized only once on server startup
@app.on_event("startup")
def startup_event():
    logger.info("Loading embedding model...")
    _ = embedding_model  # Force loading at startup
    logger.info("Embedding model loaded successfully.")


@app.post("/save_message")
async def save_message(req: MessageRequest):
    """
    Appends a message to the text file associated with a group.

    - Creates a new file if it doesn't exist.
    - Automatically adds a timestamp (UTC) if not provided.
    """

    req_group_id = req.group_id
    file_path = os.path.join(DATA_DIR, f"{req.group_id}.txt")
    timestamp = req.timestamp or datetime.utcnow().isoformat()
    try:
        async with aiofiles.open(file_path, mode='a') as f:
            await f.write(f"[{timestamp}] : {req.message}\n")
        return {"status": f"successfully saved to the message in the group id: {req_group_id}"}
    except Exception as e:
        return {"status": "error", "message": str(e)}



@app.post("/update_vectorstore")
async def update_vectorstore(request: UpdateVectorRequest):
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
async def query_vector_db(req: QueryRequest):
    """
    Sends a natural language question to the vector store for a group and gets a response using an LLM.

    - Automatically refreshes the vector store if the file has changed.
    - Uses semantic search and a language model to generate a response.
    """
    try:
        document_path = get_group_file_path(req.group_id)
        logger.info(f"Received query request for group_id='{req.group_id}'")
        if not os.path.exists(document_path):
            raise FileNotFoundError(f"No document found for group_id '{req.group_id}'")

        singleton = VectorDBSingleton(document_path=document_path, group_id=req.group_id)

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

        return{
            "response":response
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


@app.delete("/delete_group")
async def delete_group(req: DeleteRequest,request: Request):
    """
    Deletes:
    - Text file: group_texts/{groupid}.txt
    - Vector directory: vector_stores/{groupid}/
    """
    groupid = req.groupid.strip()
    txt_path = os.path.join("group_texts", f"{groupid}.txt")
    dir_path = os.path.join("vector_stores", groupid)

    # Enhanced client IP extraction
    client_host = request.client.host
    logging.info(f"Received delete request from {client_host} for groupid={groupid}")


    deleted_items = []

    # Delete .txt file
    if os.path.isfile(txt_path):
        os.remove(txt_path)
        deleted_items.append(txt_path)
        logging.info(f"Deleted file: {txt_path}")
    else:
        logging.warning(f"Text file not found: {txt_path}")

    # Delete vector store directory
    if os.path.isdir(dir_path):
        shutil.rmtree(dir_path)
        deleted_items.append(dir_path)
        logging.info(f"Deleted directory: {dir_path}")
    else:
        logging.warning(f"Directory not found: {dir_path}")

    if not deleted_items:
        raise HTTPException(status_code=404, detail=f"No existing group found in this group ID: {groupid}")

    return {
        "status": "success",
        "deleted": deleted_items,
        "requested_by": client_host,
    }

