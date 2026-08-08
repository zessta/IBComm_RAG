from fastapi import APIRouter, HTTPException
from IBComm_RAG.models.models import QueryRequest
from IBComm_RAG.services.query_from_user_handler import query_vector_logic

router = APIRouter()

@router.post(
    "/",
    summary="Query vector DB using LLM",
    description="""
    Queries the vector database using the provided query input and retrieves the most relevant documents 
    or responses by leveraging an embedding-based similarity search combined with a language model (LLM).

    This endpoint supports RAG (Retrieval-Augmented Generation) workflows by returning the most contextually 
    appropriate information based on user input.
    """,
    response_description="Query response containing matched documents or LLM-generated output."
)
async def query_vector_db(req: QueryRequest):
    """
    Handles a query request by retrieving relevant documents or information from the vector DB.

    Args:
        req (QueryRequest): Contains the query text and optional metadata such as group ID.

    Returns:
        JSON response including matched documents or generated content.
    """
    return await query_vector_logic(req)
