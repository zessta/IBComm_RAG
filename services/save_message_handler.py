import aiofiles, os
from datetime import datetime
from IBComm_RAG_api.models.models import MessageRequest

DATA_DIR = os.getenv("GROUP_TEXT_DIR", "/home/Praveen_ZT/IBComm_RAG_api/group_texts")
os.makedirs(DATA_DIR, exist_ok=True)

async def save_message_to_file(req: MessageRequest):
    file_path = os.path.join(DATA_DIR, f"{req.group_id}.txt")

    try:
        async with aiofiles.open(file_path, mode='a') as f:
            await f.write(f"{req.message}\n")
        return {"status": f"successfully saved to the message in the group id: {req.group_id}"}
    except Exception as e:
        return {"status": "error", "message": str(e)}