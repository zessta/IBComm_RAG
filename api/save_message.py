from fastapi import APIRouter
from IBComm_RAG.models.models import MessageRequest
from IBComm_RAG.services.save_message_handler import save_message_to_file

router = APIRouter()

@router.post(
    "/",
    summary="Save a message",
    description="""
    Saves a user message to a file or database under a specified group ID. 
    
    This endpoint is typically used to store messages for later retrieval or for building a context 
    that can be used with vector embeddings or LLM-based querying.
    """,
    response_description="Confirmation that the message has been saved successfully."
)
async def save_message(req: MessageRequest):
    """
    Saves a message associated with a group ID.

    Args:
        req (MessageRequest): Contains the group ID, message text, and optional metadata.

    Returns:
        JSON response indicating success or failure.
    """
    return await save_message_to_file(req)
