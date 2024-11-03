from pydantic import BaseModel
from typing import Optional


class DocumentUpload(BaseModel):
    file_type: str


class DocumentDelete(BaseModel):
    document_id: str
