from fastapi import APIRouter, Request, HTTPException
from IBComm_RAG.models.models import DeleteRequest
from IBComm_RAG.services.delete_group_handler import handle_delete

router = APIRouter()

@router.delete(
    "/",
    summary="Delete group data",
    description="""
    Deletes all stored data (messages, vector embeddings, etc.) associated with a specific group ID.
    
    Use this endpoint to completely remove a group's records from the system, 
    including any files or vectors linked to the group.
    """,
    response_description="Confirmation that the group data has been deleted successfully."
)
async def delete_group(req: DeleteRequest, request: Request):
    """
    Deletes all relevant data for a given group ID from the system.

    Args:
        req (DeleteRequest): Contains the group ID to delete.
        request (Request): FastAPI request context.

    Returns:
        JSON response with status and message.
    """
    return await handle_delete(req, request)
