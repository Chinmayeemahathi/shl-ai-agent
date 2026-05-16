# SHL AI Recommendation System

## 📌 Overview
This project is a conversational AI-powered recommendation system built for the SHL AI Internship Assignment.

The system recommends relevant SHL assessments based on:
* Job role
* Seniority
* Hiring requirements
* Follow-up refinements
* Conversational context

The project natively supports:
* Semantic search using embeddings
* Multi-turn conversations
* Clarification questions
* Assessment comparisons
* Refinement handling
* Grounded recommendations from the SHL catalog

---

## 🛠️ Tech Stack


| Technology | Purpose |
| :--- | :--- |
| **Python** | Core backend language |
| **FastAPI** | REST API framework |
| **Uvicorn** | ASGI server |
| **Sentence Transformers** | Embedding generation |
| **FAISS** | Vector similarity search |
| **JSON** | Catalog storage |
| **Swagger UI** | API testing |

---

## 🏗️ Project Architecture

```text
User Query ──> FastAPI Endpoint ──> Conversation Understanding ──> Semantic Retrieval (FAISS) ──> Boosting & Ranking Logic ──> JSON Response
```

---

## 🌟 Features

### 1. Conversational Recommendation Engine
Supports role-based recommendations, follow-up refinements, and multi-turn interactions.
* *Example Context:*
  * 👤 `"Need leadership assessments"`
  * 👤 `"CXOs with 15 years experience"`
  * 👤 `"Add cognitive assessment"`

### 2. Semantic Search
The system uses `all-MiniLM-L6-v2` embeddings combined with a **FAISS vector search**. This allows retrieval based on conceptual meaning instead of strict keyword matching.

### 3. Clarification Questions
The engine intelligently identifies vague queries and asks targeted follow-up questions.
* *Example:* `"Need leadership solution"` ──> *System asks for role/seniority clarification.*

### 4. Dynamic Refinement Support
Allows structural adjustments in real-time without losing conversation memory:
* Add cognitive tests / simulations
* Remove OPQ profiles
* Inject situational judgment tests

### 5. Comparison Mode
Supports structured, grounded structural comparisons between catalog items.
* *Example:* `"Compare OPQ Leadership Report and OPQ32r"`

### 6. Safety & Refusal Handling
The system gracefully avoids unauthorized domain guardrails (e.g., legal advice, binding hiring decisions, compliance interpretations) while keeping recommendations locked to the SHL catalog.

---

## 📂 Folder Structure

```text
SHL-AI_Agent/
│
├── app.py
├── retriever.py
├── catalog.json
├── requirements.txt
├── README.md
└── venv/
```

---

## ⚙️ Environment Setup

### Step 1: Navigate to the Project Folder
Open your standard Windows Command Prompt (`cmd`) and switch to your project drive and directory:
```cmd
D:
cd SHL-AI_Agent
```

### Step 2: Initialize the Virtual Environment
```cmd
python -m venv venv
```

### Step 3: Activate the Virtual Environment
```cmd
venv\Scripts\activate.bat
```
*(You will see `(venv)` prepended to your command line prompt upon success).*

### Step 4: Install Dependencies
```cmd
pip install fastapi uvicorn requests beautifulsoup4 sentence-transformers faiss-cpu python-dotenv pydantic
```


| Package | Purpose |
| :--- | :--- |
| `fastapi` | Backend API layer |
| `uvicorn` | High-performance ASGI web server |
| `requests` | HTTP utility client |
| `beautifulsoup4` | Web scraping and HTML parsing |
| `sentence-transformers` | Deep learning embedding generation |
| `faiss-cpu` | Efficient vector similarity search index |
| `python-dotenv` | System environment variable management |
| `pydantic` | Data validation and type enforcement |

---

## 📦 Core Subsystems

### 1. Catalog Preparation (`catalog.json`)
Stores the unified SHL catalog payload, structuring data by:
* Assessment names & descriptions
* Durations & URLs
* Test types (Adaptive vs. Standard)
* Remote delivery support infrastructure

### 2. Retriever System (`retriever.py`)
Loads raw JSON structures, executes batch calculations using `all-MiniLM-L6-v2`, initializes the local **FAISS matrix**, and injects specialized query-boosting logic to optimize matching for key domains:
* **Leadership** ──> Boosts *OPQ Profiles*
* **Graduate** ──> Boosts *Graduate Scenarios*
* **Safety** ──> Boosts *DSI Indexes*
* **Healthcare** ──> Boosts *HIPAA Modules*

### 3. FastAPI Core Layer (`app.py`)
Exposes operational endpoint routing, tracks active user state maps across conversational steps, flags boundary errors, and builds valid response schemas.

---

## 🚀 Running the Application

Start the local development server with live reload active:
```cmd
uvicorn app:app --reload
```

* **Production API Local Host:** `http://127.0.0.1:8000`
* **Interactive Swagger UI Documentation:** `http://127.0.0.1:8000/docs`

---

## 🧪 Testing Scope
The agent logic has been robustly validated against diverse domain targets, tracking historical refinement branches across:
* Leadership and Executive Hiring
* Graduate Program Pipelines
* Rust Software Engineering Requirements
* Healthcare Administration Frameworks
* Contact Center / Service Operations
* Safety-Critical Industrial Roles
* General Office Admin (Excel/Word proficiencies)

---
## Deployment Details
Deployment Live API
https://shl-ai-agent-production-763f.up.railway.app

Swagger Documentation
https://shl-ai-agent-production-763f.up.railway.app/docs

Health Endpoint
https://shl-ai-agent-production-763f.up.railway.app/health

## 🧑‍💻 Developer Info
* **Name:** Adurthi Mahathi Chinmayee
* **Project Context:** SHL AI Internship Assignment
