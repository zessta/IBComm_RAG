from pydantic import BaseModel, Field, validator
import os
from typing import Optional



class MessageRequest(BaseModel):
    group_id: str
    message: str
    timestamp: Optional[str] = None


class DeleteRequest(BaseModel):
    groupid: str = Field(..., min_length=1, max_length=100, description="Group ID of the resource to delete")


class UpdateVectorRequest(BaseModel):
    group_id: str = Field(..., min_length=1, description="Group ID")
    document_path: str = Field(..., description="Full path to the text file")

    @validator("document_path")
    def validate_path(cls, v):
        if not os.path.exists(v):
            raise ValueError(f"File does not exist: {v}")
        if not v.endswith(".txt"):
            raise ValueError("Only .txt files are supported")
        return v


class QueryRequest(BaseModel):
    group_id: str = Field(..., min_length=1, description="Group ID")
    text: str = Field(..., min_length=1, description="Query text")


