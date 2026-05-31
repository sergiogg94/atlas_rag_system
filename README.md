# Atlas RAG System

<div align="center">

![Atlas RAG](https://img.shields.io/badge/Atlas-RAG%20System-blue)
![Python](https://img.shields.io/badge/Python-3.13%2B-green)
![FastAPI](https://img.shields.io/badge/FastAPI-0.135-teal)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-blue)
![License](https://img.shields.io/badge/License-GPLv3-blue)

**Personal learning project focused on building a production-ready Retrieval-Augmented Generation (RAG) system from scratch. Used for semantic search and inteligent chat whit sources.**

[Live Demo](https://atlas-frontend-2cca.onrender.com) • [API Docs](https://atlas-backend-qgq0.onrender.com/docs) • [Dashboard](https://atlas-dashboard-pvib.onrender.com)

</div>

---
## 📋 Table of Contents

- [Overview](#-overview)
- [Tech Stack](#️-tech-stack)
- [Quick Start](#-quick-start)
- [Live Demo](#-live-demo)
- [Architecture](#-architecture)
- [Roadmap](#️-roadmap)
- [Contributing](#-contributing)
- [License](#-license)
- [Author](#-author)

---
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

---
## 🛠️ Tech Stack

### Backend
- **Framework:** FastAPI 0.135 (async)
- **Database:** PostgreSQL 16 + pgvector 0.6
- **ORM:** SQLAlchemy 2.0 (async)
- **Embeddings:** Voyage AI API 0.3
- **LLM:** HuggingFace Inference API

### Frontend
- **UI Framework:** Gradio 6.14
- **Dashboard:** Streamlit 1.57

### Infrastructure
- **Containerization:** Docker
- **Deployment:** Render (free tier)

### Development
- **Language:** Python 3.13
- **Package Manager:** uv / pip
- **Testing:** pytest
- **Linting:** ruff

---
## 🚀 Quick Start

### Prerequisites

- Python 3.13+
- Docker & Docker Compose
- HuggingFace and VoyageAi API Key

### 1. Clone the repository
```bash
git clone https://github.com/sergiogg94/atlas_rag_system.git

cd atlas_rag_system
```

### 2. Setup Environment
```bash
cp .env.example .env
```
Edit .env with your API keys and database credentials
```.env
VOYAGEAI_API_KEY=your_voyageai_api_key
HF_TOKEN=your_huggingface_api_key
DATABASE_URL=postgresql+asyncpg://USER:PASSWORD@HOST:PORT/DATABASE
```

### 3. Build and Run with Docker
```bash
# Build ans start all services (API, DB, Frontend)
docker-compose up

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```
Available services:
- Backend API: http://localhost:8000
- Swagger Docs: http://localhost:8000/docs
- Frontend: http://localhost:7860
- Dashboard: http://localhost:8501

---
## 🌐 Live Demo

### 🔗 Public URLs

| Service | URL | Description |
|---------|-----|-------------|
| **API Backend** | [atlas-backend-qgq0.onrender.com/docs](https://atlas-backend-qgq0.onrender.com/docs) | REST API + Swagger Documentation |
| **Frontend** | [atlas-frontend-2cca.onrender.com](https://atlas-frontend-2cca.onrender.com) | Gradio UI for upload & chat |
| **Dashboard** | [atlas-dashboard-pvib.onrender.com](https://atlas-dashboard-pvib.onrender.com) | Evaluation metrics & performance analysis |

> ⚠️ **Note:** Services may take ~30 seconds to "wake up" if not recently used (Render free tier).

### 🎬 Video Demo

WIP

### 📸 Screenshots

WIP

---
## 🏗️ Architecture
The Atlas RAG System is designed with a modular architecture to ensure scalability, maintainability, and ease of development.
```mermaid
flowchart TD

%% FRONTEND LAYER
subgraph Frontend_Layer["🖥️ FRONTEND LAYER"]
    direction LR
    Gradio["<b>Gradio UI</b><br/>(Port 7860)<br/>━━━━━━━━━━<br/>• Upload<br/>• Chat<br/>• Search"]
    Streamlit["<b>Streamlit Dashboard</b><br/>(Port 8501)<br/>━━━━━━━━━━<br/>• Evaluation Metrics<br/>• Performance Analysis<br/>• A/B Testing"]
end

%% BACKEND LAYER
subgraph Backend_Layer["⚙️ BACKEND LAYER"]
    Backend["<b>FastAPI Server</b><br/>━━━━━━━━━━━━━━<br/>
    <b>Endpoints:</b><br/>
    • POST /upload - Upload documents<br/>
    • POST /ingest - Ingest from text<br/>
    • POST /query - RAG query with LLM<br/>
    • POST /search - Vector similarity search<br/>
    • GET /health - Health check"]
end

%% PROCESSING LAYER
subgraph Processing_Layer["🔄 PROCESSING LAYER"]
    Processing["<b>Pipeline Components</b><br/>━━━━━━━━━━━━━━━━<br/>
    • Document Parser (PDF, TXT, MD)<br/>
    • Text Chunker (configurable size/overlap)<br/>
    • Embedding Generator (VoyageAI API)<br/>
    • LLM Integration (HuggingFace API)"]
end

%% DATA LAYER
subgraph Data_Layer["💾 DATA LAYER"]
    Data["<b>PostgreSQL 16 + pgvector</b><br/>━━━━━━━━━━━━━━━━━━━━<br/>
    • Documents table<br/>
    • Chunks table (with vector embeddings)<br/>
    • IVFFlat index for fast similarity search"]
end

%% CONNECTIONS
Frontend_Layer ==> Backend_Layer
Backend_Layer ==> Processing_Layer
Processing_Layer ==> Data_Layer

%% STYLES
classDef frontend fill:#e3f2fd,stroke:#1976d2,stroke-width:2px,color:#000
classDef backend fill:#fff3e0,stroke:#f57c00,stroke-width:2px,color:#000
classDef processing fill:#f3e5f5,stroke:#7b1fa2,stroke-width:2px,color:#000
classDef data fill:#e8f5e9,stroke:#388e3c,stroke-width:2px,color:#000

class Frontend_Layer,Gradio,Streamlit frontend
class Backend_Layer,Backend backend
class Processing_Layer,Processing processing
class Data_Layer,Data data
```

---
## 🗺️ Roadmap

**📖 For detailed development progress and technical insights, see [Development Log](./docs/development_log.md)**

### Currently Implemented

**Core Infrastructure (Weeks 1-2)**
- ✅ FastAPI REST API with async endpoints
- ✅ PostgreSQL database with pgvector extension
- ✅ SQLAlchemy ORM with connection pooling
- ✅ Comprehensive logging system

**Document Processing (Weeks 2-4)**
- ✅ Multi-format document parser (PDF, TXT, Markdown)
- ✅ Advanced text chunking with LangChain's RecursiveCharacterTextSplitter
- ✅ File upload API endpoint with validation
- ✅ Bulk upload automation

**Vector & Semantic Search (Weeks 3-5)**
- ✅ Embedding generation service (VoyageAI API)
- ✅ Vector database integration (pgvector)
- ✅ Semantic similarity search
- ✅ RAG query endpoint with source attribution

**LLM Integration (Week 5)**
- ✅ LLM service integration (HuggingFace Inference API)
- ✅ Complete end-to-end RAG pipeline
- ✅ Context-aware response generation

**Evaluation & Monitoring (Week 6)**
- ✅ Comprehensive evaluation framework
- ✅ Retrieval and generation quality metrics
- ✅ Streamlit metrics dashboard
- ✅ Test dataset with Q&A pairs

**Frontend & UI (Week 7)**
- ✅ Gradio-based interactive interface
- ✅ Multi-tab interface (Chat, Upload, Ingest, Search, Health)
- ✅ Async API client layer
- ✅ Centralized configuration management
- ✅ Custom CSS styling and branding

**Infrastructure & Deployment (Week 8)**
- ✅ Docker containerization
- ✅ Docker Compose orchestration
- ✅ Production-ready deployment configuration
- ✅ Render deployment scripts and documentation


### In Progress
- 🔄 Query rewriting and expansion
- 🔄 Response streaming

### Planned
- 📋 Hybrid search (vector + keyword)
- 📋 Observability and monitoring enhancements
- 📋 API authentication and rate limiting
- 📋 Multi-tenant support
- 📋 Caching layer for embeddings optimization

---
## 📝 Contributing

Contributions are welcome! We follow standard GitHub workflows for all contributions.

### How to Contribute

1. **Fork the repository** on GitHub
2. **Create a feature branch** for your changes:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Make your changes** and test them thoroughly
4. **Commit with clear messages** following conventional commits:
   ```bash
   git commit -m "feat: add your feature" 
   # or
   git commit -m "fix: resolve issue"
   ```
5. **Push to your fork** and create a **Pull Request**
6. **Describe your changes** clearly in the PR description
7. **Wait for review** and address any feedback

### Contribution Guidelines

- Follow PEP 8 style guide for Python code
- Add tests for new features
- Update documentation as needed
- Keep commits atomic and focused
- Be respectful and constructive in discussions

---
## 📄 License

This project is licensed under the **GNU General Public License v3.0** (GPLv3). See the [LICENSE](LICENSE) file for details.

### What this means:
- ✅ Free to use, modify, and distribute
- ✅ Must include license notice
- ✅ Must disclose source code
- ✅ Must use same license for derivatives

---
## 👤 Author

**Sergio Gutierrez Galarza**

<div align="center">

[![GitHub](https://img.shields.io/badge/GitHub-%40sergiogg94-black?style=flat-square&logo=github)](https://github.com/sergiogg94)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Sergio%20Gutierrez-blue?style=flat-square&logo=linkedin)](https://www.linkedin.com/in/sergio-gutierrez-149177215/)

</div>

📧 Email: **gutierrez.galarza.s.402@gmail.com**

This is a personal learning project developed to master RAG systems and ML engineering practices. Feel free to reach out with questions, suggestions, or collaboration ideas!

This is a personal learning project developed to master RAG systems and ML engineering practices. Feel free to reach out with questions, suggestions, or collaboration ideas!

---

**Made with ❤️ for the AI/ML community**