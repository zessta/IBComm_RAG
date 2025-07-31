import os, shutil, logging
from fastapi import HTTPException

logger = logging.getLogger(__name__)

async def handle_delete(req, request):
    groupid = req.groupid.strip()
    txt_path = os.path.join("/home/Praveen_ZT/IBComm_RAG/group_texts", f"{groupid}.txt")
    dir_path = os.path.join("/home/Praveen_ZT/IBComm_RAG/vector_stores", groupid)
    

    client_host = request.client.host
    logger.info(f"Received delete request from {client_host} for groupid={groupid}")

    deleted_items = []

    if os.path.isfile(txt_path):
        os.remove(txt_path)
        deleted_items.append(txt_path)
        logger.info(f"Deleted file: {txt_path}")
    else:
        logger.warning(f"Text file not found: {txt_path}")

    if os.path.isdir(dir_path):
        shutil.rmtree(dir_path)
        deleted_items.append(dir_path)
        logger.info(f"Deleted directory: {dir_path}")
    else:
        logger.warning(f"Directory not found: {dir_path}")

    if not deleted_items:
        raise HTTPException(status_code=404, detail=f"No existing group found in this group ID: {groupid}")

    return {
        "status": "success",
        "deleted": deleted_items,
        "requested_by": client_host,
    }