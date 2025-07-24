from fastapi import APIRouter, HTTPException
from IBComm_RAG_api.models.models import QueryRequest
from IBComm_RAG_api.services.query_from_user_handler import query_vector_logic

router = APIRouter()

@router.post("/", summary="Query vector DB using LLM")
async def query_vector_db(req: QueryRequest):
    return await query_vector_logic(req)
