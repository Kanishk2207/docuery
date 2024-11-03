-- Create users table
CREATE TABLE IF NOT EXISTS users (
    user_id VARCHAR(50) PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    created_at INTEGER,
    updated_at INTEGER
);

-- Create documents table
CREATE TABLE IF NOT EXISTS documents (
    document_id VARCHAR(50) PRIMARY KEY,
    user_id VARCHAR(50) NOT NULL,
    title VARCHAR(100) NOT NULL,
    file_url VARCHAR(255) NOT NULL,
    file_type VARCHAR(30) NOT NULL,
    uploaded_at INTEGER,
    updated_at INTEGER,
    parsed_at INTEGER,
    status VARCHAR(50) DEFAULT 'uploaded',

    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

-- Create document_metadata table
CREATE TABLE IF NOT EXISTS document_metadata (
    document_metadata_id VARCHAR(50) PRIMARY KEY,
    document_id VARCHAR(50) NOT NULL,
    key VARCHAR(100) NOT NULL,
    value TEXT NOT NULL,
    created_at INTEGER,
    updated_at INTEGER,

    FOREIGN KEY (document_id) REFERENCES documents(document_id) ON DELETE CASCADE
);

-- Create queries table
CREATE TABLE IF NOT EXISTS queries (
    query_id VARCHAR(50) PRIMARY KEY,
    user_id VARCHAR(50) NOT NULL,
    document_id VARCHAR(50),
    query_text TEXT NOT NULL,
    response_text TEXT,
    created_at INTEGER ,
    updated_at INTEGER,

    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (document_id) REFERENCES documents(document_id) ON DELETE SET NULL
);

-- Indexes for faster querying
CREATE INDEX IF NOT EXISTS idx_users_username ON users (username);
CREATE INDEX IF NOT EXISTS idx_users_email ON users (email);
CREATE INDEX IF NOT EXISTS idx_documents_user_id ON documents (user_id);
CREATE INDEX IF NOT EXISTS idx_documents_status ON documents (status);
CREATE INDEX IF NOT EXISTS idx_queries_user_id ON queries (user_id);
CREATE INDEX IF NOT EXISTS idx_queries_created_at ON queries (created_at);
