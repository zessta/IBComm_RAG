from fastapi import FastAPI
from IBComm_RAG.core.startup import load_embedding_model
from IBComm_RAG.api import delete_group,query_from_user,save_message,update_query

IBComm_RAG = FastAPI(
    title="IBComm RAG API",
    description=(
        "An API backend for managing group-based document interactions powered by Retrieval-Augmented Generation (RAG). "
        "Supports saving user messages, updating and persisting vector embeddings, querying semantically across stored content using LLMs, "
        "and deleting all group-associated data when a group is removed from the chat. "
        "Designed to enable intelligent, context-aware document search and interaction."
    ),
    version="1.0.0",
    docs_url="/v1/docs",
    redoc_url="/v1/redoc"
)

@IBComm_RAG.on_event("startup")
def startup_event():
    load_embedding_model()

IBComm_RAG.include_router(save_message.router, prefix="/save_message", tags=["Group Messaging"])
IBComm_RAG.include_router(update_query.router, prefix="/update_vectorstore", tags=["Vector Store"])
IBComm_RAG.include_router(query_from_user.router, prefix="/query", tags=["Query"])
IBComm_RAG.include_router(delete_group.router, prefix="/delete_group", tags=["Group delete"])
