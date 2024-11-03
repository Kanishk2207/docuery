from sqlalchemy import Column, String, Integer, Text, ForeignKey, Index
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.internal.model.base import DBBase as Base
# from sqlalchemy.ext.declarative import declarative_base

# Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    user_id: Mapped[str] = mapped_column(String(50), primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[int] = mapped_column(Integer)
    updated_at: Mapped[int] = mapped_column(Integer)

    documents = relationship('Document', back_populates='user')
    queries = relationship('Query', back_populates='user')

    __table_args__ = (
        Index('idx_users_username', 'username'),
        Index('idx_users_email', 'email'),
    )


class Document(Base):
    __tablename__ = 'documents'

    document_id: Mapped[str] = mapped_column(String(50), primary_key=True)
    user_id: Mapped[str] = mapped_column(String(50), ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    file_path: Mapped[str] = mapped_column(String(255), nullable=False)
    file_type: Mapped[str] = mapped_column(String(10), nullable=False)
    uploaded_at: Mapped[int] = mapped_column(Integer)
    updated_at: Mapped[int] = mapped_column(Integer)
    parsed_at: Mapped[int] = mapped_column(Integer)
    status: Mapped[str] = mapped_column(String(50), default='uploaded')

    user = relationship('User', back_populates='documents')
    document_metadata = relationship('DocumentMetadata', back_populates='document')
    queries = relationship('Query', back_populates='document')

    __table_args__ = (
        Index('idx_documents_user_id', 'user_id'),
        Index('idx_documents_status', 'status'),
    )


class DocumentMetadata(Base):
    __tablename__ = 'document_metadata'

    document_metadata_id: Mapped[str] = mapped_column(String(50), primary_key=True)
    document_id: Mapped[str] = mapped_column(String(50), ForeignKey('documents.document_id', ondelete='CASCADE'), nullable=False)
    key: Mapped[str] = mapped_column(String(100), nullable=False)
    value: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[int] = mapped_column(Integer)
    updated_at: Mapped[int] = mapped_column(Integer)

    document = relationship('Document', back_populates='document_metadata')


class Query(Base):
    __tablename__ = 'queries'

    query_id: Mapped[str] = mapped_column(String(50), primary_key=True)
    user_id: Mapped[str] = mapped_column(String(50), ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False)
    document_id: Mapped[str] = mapped_column(String(50), ForeignKey('documents.document_id', ondelete='SET NULL'))
    query_text: Mapped[str] = mapped_column(Text, nullable=False)
    response_text: Mapped[str] = mapped_column(Text)
    created_at: Mapped[int] = mapped_column(Integer)
    updated_at: Mapped[int] = mapped_column(Integer)

    user = relationship('User', back_populates='queries')
    document = relationship('Document', back_populates='queries')

    __table_args__ = (
        Index('idx_queries_user_id', 'user_id'),
        Index('idx_queries_created_at', 'created_at'),
    )
