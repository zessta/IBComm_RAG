from fastapi import APIRouter
from IBComm_RAG.models.models import MessageRequest
from IBComm_RAG.services.save_message_handler import save_message_to_file

router = APIRouter()

@router.post("/", summary="Save a message")
async def save_message(req: MessageRequest):
    return await save_message_to_file(req)