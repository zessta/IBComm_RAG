from fastapi import APIRouter, Request, HTTPException
from IBComm_RAG_api.models.models import DeleteRequest
from IBComm_RAG_api.services.delete_group_handler import handle_delete

router = APIRouter()

@router.delete("/", summary="Delete group data")
async def delete_group(req: DeleteRequest, request: Request):
    return await handle_delete(req, request)
