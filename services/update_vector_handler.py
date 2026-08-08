import os, traceback, logging
from fastapi import HTTPException
from IBComm_RAG.services.vector_store import VectorDBSingleton

logger = logging.getLogger(__name__)

async def update_vector_logic(request):
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