# Self-Correcting Reliability RAG Agent 🤖

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat&logo=python)
![LangChain](https://img.shields.io/badge/LangChain-Orchestration-green?style=flat)
![Status](https://img.shields.io/badge/Status-In%20Progress-orange)

## 📌 Project Overview
**Targeting Uncertainty in AI:** This project is an intelligent QA agent designed to handle unstructured technical documentation (PDFs, Manuals) with high reliability. It implements a **"Self-Reflective" Multi-Agent workflow** where a 'Critic' evaluates the retrieved information to minimize hallucinations.

## 🚀 Key Features
- **Self-Correction Loop:** Automatically detects low-confidence answers via LLM evaluation and triggers re-retrieval.
- **Semantic Router:** Dynamically routes queries based on complexity (Simple Lookup vs. Complex Reasoning).
- **Unstructured Data Parsing:** Robust ingestion pipeline for messy engineering PDFs.

## 🛠 Tech Stack
- **Core:** Python, LangChain, OpenAI API
- **Database:** ChromaDB (Vector Store)
- **UI:** Streamlit

## 🚧 Development Roadmap
- [x] Initial Architecture Design
- [ ] PDF Ingestion Pipeline Setup
- [ ] Multi-Agent Logic Implementation (LangGraph)
- [ ] UI/UX with Streamlit
      
## 🏗 Architecture (Concept)
```mermaid
graph LR
A[User Query] --> B{Semantic Router}
B -- Simple --> C[Vector Search]
B -- Complex --> D[Agentic Search]
C --> E{Critic Agent}
D --> E
E -- High Confidence --> F[Final Answer]
E -- Low Confidence --> G[Fallback / Retry]
