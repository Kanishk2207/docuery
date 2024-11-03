import time
from sqlalchemy.ext.asyncio import AsyncSession
from app.internal import crud
from app.external.gcp.gcs_client import GCSClient
from app.internal.model.model import Document
from app.utils.uuid_utils import get_uuid
from app.internal.db.postgres import get_db

current_time = time.time()

async def upload_document(file, user_id: str):
    """
    Upload a document to Google Cloud Storage and save metadata in the database.
    """

    global current_time

    gcs_client = GCSClient()

    file_url = gcs_client.upload_file(file)

    document_id = get_uuid()

    new_document = Document(
        document_id =  document_id,
        user_id =  user_id,
        title =  file.filename,
        file_url =  file_url,
        file_type =  file.content_type,
        uploaded_at =  current_time,
        updated_at =  current_time,
        parsed_at =  current_time,
    )
    async with get_db() as db:
        document = await crud.create_document(db, new_document=new_document)

    return document

# Function to retrieve a document by ID
async def get_document( document_id: str, user_id: str):
    """
    Retrieve a document by ID if it belongs to the authenticated user.
    """
    async with get_db() as db:
        document = await crud.get_document_by_id(db, document_id)
    
    if not document or document.user_id != user_id:
        return None
    
    return document

async def get_all_documents_for_user(user_id: str):

    async with get_db() as db:
        documents = await crud.get_documents_by_user(db=db, user_id=user_id)
    
    return documents

# Function to delete a document by ID
async def delete_document(db: AsyncSession, document_id: str, user_id: str):
    """
    Delete a document by ID from GCS and database.
    """
    document = await crud.get_document_by_id(db, document_id)
    
    if not document or document.user_id != user_id:
        return None

    delete_file_from_gcs(document.file_url)
    await crud.delete_document(db, document_id)

    return True
