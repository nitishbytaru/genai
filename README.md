# Generative AI Playground & Agent Architectures 🤖

A comprehensive monorepo showcasing modern Generative AI engineering patterns, autonomous agents, Retrieval-Augmented Generation (RAG), graph memory systems, asynchronous queue architectures, and end-to-end voice agents using the Google Gemini ecosystem.

---

## 📑 Table of Contents

- [Overview](#overview)
- [Repository Structure](#repository-structure)
- [Projects & Modules](#projects--modules)
  - [1. Memory Agent (`mem_agent/`)](#1-memory-agent-mem_agent)
  - [2. Weather Tool-Calling Agent (`weather-agent/`)](#2-weather-tool-calling-agent-weather-agent)
  - [3. PDF RAG Assistant (`rag/`)](#3-pdf-rag-assistant-rag)
  - [4. Asynchronous Queue RAG (`rag_queue/`)](#4-asynchronous-queue-rag-rag_queue)
  - [5. LangGraph Experiments (`learning_langgraph/`)](#5-langgraph-experiments-learning_langgraph)
  - [6. Voice Assistant (`voice_agent/`)](#6-voice-assistant-voice_agent)
- [Tech Stack](#tech-stack)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Environment Variables](#environment-variables)
- [Running the Projects](#running-the-projects)

---

## 🌟 Overview

This repository demonstrates practical implementations of modern LLM applications:

- **Stateful Memory**: Hybrid vector + knowledge graph memory extraction using Mem0, Qdrant, and Neo4j.
- **Function / Tool Calling**: Grounded agents invoking external APIs with Pydantic schema validation.
- **Retrieval-Augmented Generation (RAG)**: Chunking, embedding, vector search, and context-grounded citations.
- **Asynchronous Architecture**: Production-style decoupling of heavy LLM inferences via task queues (Python RQ & Valkey/Redis) behind FastAPI.
- **Graph State Machines**: Cyclical and conditional agent workflows built on LangGraph.
- **Conversational Voice Agent**: Real-time voice interaction loop combining Speech-to-Text (STT), Gemini LLM dialogue, and Gemini Audio/TTS playback.

---

## 📂 Repository Structure

```text
genai/
├── mem_agent/                  # Persistent memory agent (Mem0 + Qdrant + Neo4j)
│   ├── mem.py                  # Interactive memory management CLI
│   └── docker-compose.yml      # Qdrant vector database container
│
├── weather-agent/              # Agent with function calling & weather tool
│   ├── app/
│   │   ├── agent.py            # Gemini chat session with tool binding
│   │   ├── weather.py          # Open-Meteo API integration & geocoding
│   │   └── schemas.py          # Pydantic models for structured weather data
│   ├── test_agent.py           # Interactive CLI chat
│   └── requirments.txt         # Module dependencies
│
├── rag/                        # Interactive PDF RAG assistant
│   ├── index.py                # PDF parser, chunker, & vector store indexer
│   ├── chat.py                 # Terminal chat interface with cited answers
│   └── docker-compose.yml      # Qdrant service configuration
│
├── rag_queue/                  # Scalable asynchronous RAG with FastAPI & RQ
│   ├── server.py               # FastAPI API endpoints (/chat, /get-status)
│   ├── main.py                 # Uvicorn server launcher
│   ├── client/rq_client.py     # Redis/Valkey queue connection
│   ├── queues/worker.py        # Background task processor for RAG queries
│   └── docker-compose.yml      # Valkey (Redis-compatible) cache/broker
│
├── voice_agent/                # Real-time voice interaction agent
│   ├── main.py                 # Mic capture, Google STT, Gemini chat, & TTS playback
│   └── response.wav            # Generated audio output buffer
│
├── learning_langgraph/         # LangGraph state machine prototypes
│   ├── chat.py                 # Sequential state graph with message history
│   └── chat_2.py               # Conditional branching & multi-node execution
│
├── requirments.txt             # Unified workspace dependencies
└── README.md                   # Repository documentation
```

---

## 🚀 Projects & Modules

### 1. Memory Agent (`mem_agent/`)
An intelligent personal memory system built on the **Mem0** framework:
- **Hybrid Storage**: Combines **Qdrant** for semantic vector similarity with **Neo4j** for relational knowledge graphs.
- **Gemini Powered**: Employs `models/gemini-embedding-001` (768 dimensions) for embeddings and Gemini models for fact extraction.
- **Capabilities**: Extract facts, preferences, and relationships from conversations and query memories across sessions.

### 2. Weather Tool-Calling Agent (`weather-agent/`)
A grounded conversational assistant leveraging native **Gemini Function Calling**:
- **Tool Integration**: Resolves city names to coordinates via Open-Meteo Geocoding and fetches live meteorological data.
- **Strict Guardrails**: Validates payloads with **Pydantic**, rejects out-of-scope inquiries, and formats replies with structured weather metrics (temperature, feels-like, humidity, wind speed).

### 3. PDF RAG Assistant (`rag/`)
A semantic search and document question-answering assistant:
- **Pipeline**: Ingests PDFs using LangChain's `PyPDFLoader`, splits documents into overlapping chunks with `RecursiveCharacterTextSplitter`, and indexes them in **Qdrant**.
- **Context Grounding**: Constrains Gemini to answer strictly from the retrieved document context while citing page numbers and source metadata.
- **Terminal UI**: Features an interactive typewriter-style terminal output.

### 4. Asynchronous Queue RAG (`rag_queue/`)
Production-grade architecture pattern to prevent API timeouts during slow RAG inference:
- **FastAPI Endpoints**:
  - `POST /chat?query=...` — Pushes user query into the queue and returns an immediate `job_id`.
  - `GET /get-status?job_id=...` — Polls job state and returns the completed RAG response.
- **Queue Broker**: Uses **Python RQ** paired with **Valkey** (high-performance Redis alternative).
- **Decoupled Worker**: Dedicated background worker runs vector similarity search and LLM generation.

### 5. LangGraph Experiments (`learning_langgraph/`)
State-driven agent architectures using **LangGraph**:
- `chat.py`: Linear graph chaining nodes through message state reducers (`add_messages`).
- `chat_2.py`: Conditional graph flow evaluating node output to determine whether to loop or terminate.

### 6. Voice Assistant (`voice_agent/`)
An end-to-end interactive voice agent with audio in / audio out:
- **Speech Recognition (STT)**: Listens to the microphone using `speech_recognition` with customizable energy threshold and device indexing, transcribing voice via Google Speech Recognition.
- **Conversational Intelligence**: Routes transcribed queries to Gemini Chat (`google-genai` SDK) instructed to reply naturally and conversationally.
- **Text-to-Speech (TTS) & Playback**: Generates spoken audio using Gemini's native audio response capabilities (`response_modalities=["AUDIO"]`, prebuilt voice `Kore`), saves the stream as a WAV file, and plays it back through the system speaker (`aplay`).

---

## 🛠 Tech Stack

| Category | Technologies |
| :--- | :--- |
| **LLMs & Embeddings** | Google Gemini 2.5 / 2.0 / 1.5, `google-genai` SDK, `langchain-google-genai` |
| **Agent Frameworks** | LangChain, LangGraph, Mem0 |
| **Speech & Audio** | SpeechRecognition, PyAudio, Gemini Native Audio/TTS, ALSA (`aplay`) |
| **Databases & Stores** | Qdrant (Vector DB), Neo4j (Graph DB), Valkey / Redis |
| **Backend & Queues** | FastAPI, Uvicorn, Python RQ, HTTPX |
| **Data & Parsing** | Pydantic v2, PyPDF, LangChain Text Splitters |
| **Containerization** | Docker, Docker Compose |

---

## ⚙️ Getting Started

### Prerequisites

- Python 3.10+ (Recommended: 3.11+)
- Docker & Docker Compose
- Google Gemini API Key ([Google AI Studio](https://aistudio.google.com/))
- System Audio & Mic Utilities:
  - Linux: `alsa-utils` (provides `aplay`), `portaudio19-dev` (for `PyAudio`)
- Neo4j Instance (optional, for `mem_agent`)

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/nitishbytaru/genai.git
   cd genai
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install system audio dependencies (if running `voice_agent` on Linux):**
   ```bash
   sudo apt-get update && sudo apt-get install -y alsa-utils portaudio19-dev
   ```

4. **Install Python dependencies:**
   ```bash
   pip install -r requirments.txt
   ```

### Environment Variables

Create a `.env` file in each module directory (or in root as required). A template for the variables:

```env
# Google Gemini Configuration
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-2.0-flash

# Neo4j Graph DB (Required for mem_agent)
NEO4J_URI=bolt://localhost:7687
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=your_password
```

> **Note:** `.env` files are excluded from Git via `.gitignore`. Never commit API keys.

---

## 🏃 Running the Projects

### Running the Voice Assistant (`voice_agent`)
```bash
cd voice_agent
python main.py
```

### Running the Memory Agent (`mem_agent`)
```bash
# Start Qdrant vector database
cd mem_agent
docker compose up -d

# Run the memory agent CLI
python mem.py
```

### Running the Weather Agent (`weather-agent`)
```bash
cd weather-agent
python test_agent.py
```

### Running the RAG Assistant (`rag`)
```bash
cd rag
# 1. Start Qdrant
docker compose up -d

# 2. Ingest & index the document
python index.py

# 3. Query the assistant
python chat.py
```

### Running Asynchronous RAG (`rag_queue`)
```bash
cd rag_queue
# 1. Start Valkey / Redis
docker compose up -d

# 2. In a separate terminal, start the RQ worker
rq worker --with-scheduler

# 3. Start the FastAPI server
python -m rag_queue.main
# Server runs at: http://localhost:8000 (Docs: http://localhost:8000/docs)
```

### Running LangGraph Examples (`learning_langgraph`)
```bash
cd learning_langgraph
python chat.py
python chat_2.py
```
