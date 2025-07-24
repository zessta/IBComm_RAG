from fastapi import APIRouter, HTTPException
from IBComm_RAG_api.models.models import UpdateVectorRequest
from IBComm_RAG_api.services.update_vector_handler import update_vector_logic

router = APIRouter()

@router.post("/", summary="Update vector store")
async def update_vectorstore(request: UpdateVectorRequest):
    return await update_vector_logic(request)
