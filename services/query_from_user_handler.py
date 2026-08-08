import os, logging, traceback
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from IBComm_RAG.services.vector_store import VectorDBSingleton
from IBComm_RAG.services.llama_call import chat_with_model
from IBComm_RAG.utils.get_path import get_group_file_path

logger = logging.getLogger(__name__)

async def query_vector_logic(req):
    try:
        document_path = get_group_file_path(req.group_id)
        logger.info(f"Received query request for group_id='{req.group_id}'")

        if not os.path.exists(document_path):
            return JSONResponse(
                status_code=500,
                content={"Group id not found": f"No document found for group_id '{req.group_id}'"}
            )

        singleton = VectorDBSingleton(document_path=document_path, group_id=req.group_id)
        updated = singleton.update_vectorstore_if_needed()

        if updated:
            logger.info(f"Vector store updated for group_id='{req.group_id}'")

        vs = singleton.get_vectorstore()
        retriever = vs.as_retriever(search_kwargs={"k": 3})
        docs = retriever.get_relevant_documents(req.text)

        if not docs:
            raise HTTPException(status_code=404, detail="No relevant documents found.")

        results = [doc.page_content for doc in docs]
        response = chat_with_model(text=results, query=req.text)

        return {"response": response}

    except ValueError as ve:
        logger.error(f"Validation error: {ve}")
        raise HTTPException(status_code=400, detail=str(ve))
    except FileNotFoundError as fe:
        logger.error(f"File not found: {fe}")
        raise HTTPException(status_code=404, detail=str(fe))
    except Exception as e:
        logger.error("Unhandled exception occurred:")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail="Internal server error")
