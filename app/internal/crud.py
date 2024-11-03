from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import delete, update
from app.internal.model.model import User, Document, DocumentMetadata, Query 
from app.utils.uuid_utils import get_uuid


# Create operations
async def create_user(db: AsyncSession, new_user: User):
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

async def create_document(db: AsyncSession, user_id: int, title: str, file_path: str, file_type: str, status: str):
    document_id = get_uuid()
    new_document = Document(document_id=document_id, user_id=user_id, title=title, file_path=file_path, file_type=file_type, status=status)
    db.add(new_document)
    await db.commit()
    await db.refresh(new_document)
    return new_document

# Read operations
async def get_user_by_id(db: AsyncSession, user_id: int):
    result = await db.execute(select(User).filter(User.id == user_id))
    return result.scalars().first()

async def get_user_by_email(db: AsyncSession, email: str):
    result = await db.execute(select(User).filter(User.email == email))
    return result.scalars().one_or_none()

async def get_documents_by_user(db: AsyncSession, user_id: int):
    result = await db.execute(select(Document).filter(Document.user_id == user_id))
    return result.scalars().all()

# Update operations
async def update_document_status(db: AsyncSession, document_id: int, new_status: str):
    await db.execute(update(Document).where(Document.id == document_id).values(status=new_status))
    await db.commit()

# Delete operations
async def delete_user(db: AsyncSession, user_id: int):
    await db.execute(delete(User).where(User.id == user_id))
    await db.commit()
