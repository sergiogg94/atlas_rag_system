# Atlas RAG System

<div aling="center">

![Atlas RAG](https://img.shields.io/badge/Atlas-RAG%20System-blue)
![Python](https://img.shields.io/badge/Python-3.13%2B-green)
![FastAPI](https://img.shields.io/badge/FastAPI-0.135-teal)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-blue)
![License](https://img.shields.io/badge/License-GPLv3-blue)

**Personal learning project focused on building a production-ready Retrieval-Augmented Generation (RAG) system from scratch. Used for semantic search and inteligent chat whit sources.**

[Live Demo](https://atlas-frontend-2cca.onrender.com) • [API Docs](https://atlas-backend-qgq0.onrender.com/docs) • [Dashboard](https://atlas-dashboard-pvib.onrender.com)

</div>

## 📋 Table of Contents

- [Overview](#-overview)
- [Tech Stack](#️-tech-stack)
- [Roadmap](#️-roadmap)

## 📝 Overview

This is a personal learning project focused on building a production-ready
Retrieval-Augmented Generation (RAG) system from scratch.
The goal is to deeply understand the entire technology stack required
for modern AI applications.

**Atlas RAG System lets you:**
- 📤 **Upload and process** documents (PDF, TXT, MD)
- 🔍 **Semantic search** using vector embeddings
- 💬 **Intelligent chat** with your documents using LLMs
- 📊 **Systematic evaluation** with multiple metrics
- 🎯 **Production deployment** with Render

**Use cases:**
- Internal company knowledge bases
- Q&A systems for technical documentation
- Specialized virtual assistants
- Analysis and search in large text volumes

**Why this project?**
- Master FastAPI for building high-performance APIs
- Learn vector databases and semantic search with pgvector
- Understand RAG architecture at a fundamental level
- Build portfolio-worthy AI infrastructure
- Gain practical ML engineering experience

## 🛠️ Tech Stack

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

## 🗺️ Roadmap

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