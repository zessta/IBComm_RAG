from fastapi import APIRouter, HTTPException
from IBComm_RAG.models.models import QueryRequest
from IBComm_RAG.services.query_from_user_handler import query_vector_logic

router = APIRouter()

@router.post("/", summary="Query vector DB using LLM")
async def query_vector_db(req: QueryRequest):
    return await query_vector_logic(req)
