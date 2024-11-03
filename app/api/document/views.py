from fastapi import APIRouter, Depends, HTTPException, status, UploadFile
from app.api.document.model import DocumentUpload
from app.api.document.service import upload_document, get_document, get_all_documents_for_user
from app.dependencies import AuthValidator
from app.utils.jwt_utils import __user_model

router = APIRouter(tags=["documents"])

@router.post("/documents", dependencies=[Depends(AuthValidator())],)
async def upload_document_endpoint(
    file: UploadFile,
    jwt_token: str = Depends(AuthValidator())
    ):

    user = __user_model(jwt_token)
    user_id = user.get("user_id")

    created_document = await upload_document(user_id=user_id, file=file)

    return created_document


@router.get("/documents/all", dependencies=[Depends(AuthValidator())])
async def get_all_documens(
    jwt_token: str = Depends(AuthValidator())
    ):

    user = __user_model(jwt_token)
    user_id = user.get("user_id")

    document = await get_all_documents_for_user(user_id=user_id)

    return document

@router.get("/documents/{document_id}", dependencies=[Depends(AuthValidator())])
async def get_document_by_document_id(
    document_id: str, 
    jwt_token: str = Depends(AuthValidator())
    ):

    user = __user_model(jwt_token)
    user_id = user.get("user_id")

    document = await get_document(document_id=document_id, user_id=user_id)
    if document.user_id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
    return document
