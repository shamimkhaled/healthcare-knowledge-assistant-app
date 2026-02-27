# Acme AI LLM Engineer — Technical Test Guide

This document summarizes the job description, technical test requirements, implementation plan, and tips for the Acme AI LLM Engineer position.

---

## Table of Contents

1. [Job Description](#job-description)
2. [Technical Test Overview](#technical-test-overview)
3. [Tasks & Scoring Criteria](#tasks--scoring-criteria)
4. [Deliverables](#deliverables)
5. [Submission Requirements](#submission-requirements)
6. [Implementation Plan](#implementation-plan)
7. [Tips & Best Practices](#tips--best-practices)

> **For detailed step-by-step development instructions, see [DEVELOPMENT_GUIDE.md](DEVELOPMENT_GUIDE.md).**

---

## Job Description

### Role
**Senior LLM Engineer** — Strong backend focus, working with global AI companies.

### Key Responsibilities
- Design and develop Python-based backend services (FastAPI / Flask) for LLM-based RAG systems and data engines
- Build and optimise document ingestion, embedding, retrieval and generation pipelines using vector databases (PG Vector, FAISS, Pinecone)
- Develop and optimise RAG workflows, including document chunking, context retrieval, and response generation
- Integrate and orchestrate LLM providers (OpenAI, Anthropic, Azure OpenAI) through LangChain or custom orchestration layers
- Build and optimise APIs for documentation, retrieval and generation
- Implement NL2SQL pipelines (baseline and agentic) for natural-language-to-query conversion and visualisation suggestion
- Ensure scalability, reliability, and security of Python services deployed on AWS (ECS, Lambda, S3, RDS) and MS Azure
- Ensure data privacy, security and compliance across backend systems
- Monitor performance, latency, and cost of LLM calls, embeddings, and retrieval operations
- Collaborate closely with the Controller (Node.js) team to align orchestration and response pipelines
- Lead code reviews, unit testing, and CI/CD automation for Python-based backend components
- Document APIs and backend workflows, ensuring clarity for frontend and data engineering teams

### Experience & Qualification
- 5–7 years of backend engineering experience with Python (FastAPI, Flask, or Django)
- Proven experience building LLM-integrated RAG systems or AI-driven backend architecture
- Strong understanding of vector databases (PGVector, FAISS, Pinecone, Weaviate) and embedding models
- Hands-on experience with LangChain, LlamaIndex, or similar LLM orchestration frameworks
- Strong knowledge of AWS services (ECS, Lambda, S3, RDS, CloudWatch) and CI/CD pipelines
- Familiarity with prompt engineering, token optimisation and multi-model LLM orchestration
- Knowledge of data processing workflows (CSV/XLS ingestion, schema parsing, SQL query generation)
- Commitment to best practices in code quality, security, and cloud-native design

### Nice to Have
- Experience with agentic LLM pipelines (multi-step reasoning and tool use)
- Familiarity with multi-tenant architectures and event-driven systems (SQS, SNS, Kafka)
- Knowledge of MLOps / LLMOps practices for monitoring and fine-tuning model usage
- Background in data visualisation APIs or analytics-driven query generation
- Experience in Microsoft Azure services and technologies

### Work Details
- **Type:** Full-time, onsite with some remote flexibility
- **Schedule:** Standard 8 hours, five-days engagement
- **Location:** Acme AI Ltd, Level 5, House 385, Road 6, Mirpur DOHS, Dhaka 1216
- **Salary:** BDT 80,000–130,000 (based on experience and test results)

---

## Technical Test Overview

### Scenario: Healthcare Knowledge Assistant
Build a backend for a RAG-powered assistant that helps clinicians retrieve medical guidelines and research summaries in **English** and **Japanese**. The system must:
- Ingest documents in either language
- Respond to queries in either language (e.g., *"What are the latest recommendations for Type 2 diabetes management?"*)

### Time Limit
**3 hours**

---

## Tasks & Scoring Criteria

| Section | Task Description | Weight |
|---------|------------------|--------|
| **Setup** | Initialise a FastAPI project with FAISS and sentence-transformers | — |
| **Ingestion** | `/ingest` — Accept `.txt` documents in English or Japanese. Detect language, generate embeddings, and store in FAISS | — |
| **Retrieval Endpoint** | `/retrieve` — Accept a query in English or Japanese. Return top-3 relevant documents with similarity scores | 15% |
| **Generation Endpoint** | `/generate` — Combine retrieved docs + query into a mock LLM response. Support bilingual output (same as query language) | 15% |
| **Translation Feature** | Add optional translation toggle (e.g., `output_language: "en"` or `"ja"`). Use a mock or open-source translation tool (e.g., transformers or googletrans) | 15% |
| **Security** | Implement API key authentication (`X-API-Key` header) | 10% |
| **Deployment** | Implement an automatic CI/CD pipeline with GitHub Actions and Docker | 10% |
| **Design Notes** | Write 1–2 paragraphs on scalability, modularity, and future improvements | 10% |
| **Code structure & clarity** | — | 15% |
| **Documentation & packaging** | — | 10% |

---

## Deliverables

1. **Source code** — Modular, clean structure
2. **README** — Setup instructions and design notes
3. **GitHub Actions & Dockerfile** — Automated CI/CD and containerisation

---

## Submission Requirements

| Item | Requirement |
|------|-------------|
| **Format** | Single PDF document containing all tasks, code files, and written responses |
| **File name** | `LLM-AAI-[Your Full Name].pdf` |
| **External references** | Include as hyperlinks within the document |
| **Submission** | Upload to the Google Form (link provided in original test document) |
| **Deadline** | **28 February 2026, 10:00 AM** |

### AI Usage Disclaimer
- Use of AI tools (e.g., Copilot, ChatGPT, Gemini) is **strictly prohibited** unless explicitly stated
- If any AI-generated content is used (e.g., mock responses, code snippets), it **must be cited clearly**
- Submissions may be verified with AI detection tools; undisclosed AI-generated content may result in disqualification

---

## Implementation Plan

### Phase 1: Setup (~20 min)
1. Create FastAPI project structure
2. Add dependencies: `fastapi`, `uvicorn`, `faiss-cpu`, `sentence-transformers`, `langdetect` (or `googletrans`/`transformers` for translation)
3. Set up language detection for documents and queries

### Phase 2: Core RAG Logic (~45 min)
1. **`/ingest` endpoint**
   - Accept `.txt` file uploads
   - Detect language with `langdetect`
   - Use multilingual embedding model (e.g., `paraphrase-multilingual-MiniLM-L12-v2`)
   - Store embeddings in FAISS and persist index

2. **`/retrieve` endpoint**
   - Accept query string
   - Embed query with same model
   - Search FAISS for top-3, return chunks with similarity scores

3. **`/generate` endpoint**
   - Take query + retrieved docs
   - Produce mock LLM response (e.g., "Based on the retrieved documents: ...")
   - Output in same language as query

### Phase 3: Extra Features (~35 min)
1. **Translation**
   - Add optional `output_language` parameter to `/generate` (e.g., in request body)
   - Use `googletrans` or a small `transformers` model for EN↔JA translation

2. **Security**
   - Add API key validation via dependency injection
   - Validate `X-API-Key` header on all protected endpoints

### Phase 4: DevOps (~40 min)
1. **Docker**
   - Write `Dockerfile` with Python base image, install dependencies, run FastAPI with `uvicorn`

2. **GitHub Actions**
   - Workflow: checkout → build Docker image → (optionally) run tests and lint

### Phase 5: Polish (~30 min)
1. **Design notes**
   - Write 1–2 paragraphs covering:
     - **Scalability:** Async handling, caching, separate embedding service
     - **Modularity:** Routers, services, config separation
     - **Future improvements:** Real LLM integration, PG Vector, monitoring

2. **README**
   - Setup instructions, environment variables, API examples, design notes summary

3. **Code quality**
   - Ensure clean structure, `requirements.txt`, type hints, docstrings

---

## Tips & Best Practices

- **Multilingual embeddings:** Use `paraphrase-multilingual-MiniLM-L12-v2` or similar for English and Japanese
- **Modular structure:** Separate routers, services, and config (e.g., `app/`, `services/`, `routers/`)
- **Test early:** Validate each endpoint (e.g., with `curl` or a simple script) before finalising
- **Prioritise:** Get a minimal working version first, then add translation and security
- **Design notes:** Be specific about scalability and modularity rather than generic

---

*Last updated: February 2026*
