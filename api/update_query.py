from fastapi import APIRouter, HTTPException
from IBComm_RAG.models.models import UpdateVectorRequest
from IBComm_RAG.services.update_vector_handler import update_vector_logic

router = APIRouter()

@router.post(
    "/",
    summary="Update vector store",
    description="""
    Updates the vector store with new documents or content associated with a specific group ID.

    This endpoint is used to process the provided text (e.g., from uploaded files or raw input), 
    generate vector embeddings, and update the underlying vector database for future semantic search or RAG queries.
    """,
    response_description="Confirmation that the vector store has been updated successfully."
)
async def update_vectorstore(request: UpdateVectorRequest):
    """
    Updates the vector store with embeddings generated from provided documents.

    Args:
        request (UpdateVectorRequest): Contains group ID, document paths or text, and metadata.

    Returns:
        JSON response indicating the status of the vector store update.
    """
    return await update_vector_logic(request)
