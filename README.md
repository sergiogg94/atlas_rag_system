# ATLAS RAG System

## Project Overview

This is a personal learning project focused on building a production-ready
Retrieval-Augmented Generation (RAG) system from scratch.
The goal is to deeply understand the entire technology stack required
for modern AI applications.

**Why this project?**
- Master FastAPI for building high-performance APIs
- Learn vector databases and semantic search with pgvector
- Understand RAG architecture at a fundamental level
- Build portfolio-worthy AI infrastructure
- Gain practical ML engineering experience

## Tech Stack

### Core Framework
- **FastAPI**: High-performance async web framework
- **Pydantic**: Data validation and settings management
- **Uvicorn**: Lightning-fast ASGI server

### Database & Vector Search
- **PostgreSQL 16**: Robust relational database
- **pgvector**: Vector similarity search extension
- **asyncpg**: Async PostgreSQL driver

### AI/ML Components
- **Sentence Transformers**: Document embeddings
- **OpenAI API**: LLM integration (planned)
- **LangChain**: RAG orchestration (planned)

### Development Tools
- **Docker**: Containerization
- **pytest**: Testing framework
- **black/ruff**: Code formatting and linting

## Features

### Currently Implemented
- ✅ FastAPI REST API with async endpoints
- ✅ PostgreSQL database with pgvector extension
- ✅ Document ingestion pipeline
- ✅ Vector embedding generation
- ✅ Semantic similarity search
- ✅ Basic RAG query endpoint

### In Progress
- 🔄 Advanced chunking strategies
- 🔄 Multi-document query support
- 🔄 Caching layer for embeddings
- 🔄 API authentication and rate limiting

### Planned
- 📋 Hybrid search (vector + keyword)
- 📋 Query rewriting and expansion
- 📋 Response streaming
- 📋 Observability and monitoring
- 📋 Multi-tenant support
- 📋 Containerized deployment