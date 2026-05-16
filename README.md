# shl-ai-agent
# SHL AI Recommendation System

## Overview

This project is a conversational AI-powered recommendation system built for the SHL AI Internship Assignment.

The system recommends relevant SHL assessments based on:
- job role
- seniority
- hiring requirements
- follow-up refinements
- conversational context

The project supports:
- semantic search using embeddings
- multi-turn conversations
- clarification questions
- assessment comparisons
- refinement handling
- grounded recommendations from SHL catalog

---

# Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core backend language |
| FastAPI | REST API framework |
| Uvicorn | ASGI server |
| Sentence Transformers | Embedding generation |
| FAISS | Vector similarity search |
| JSON | Catalog storage |
| Swagger UI | API testing |

---

# Project Architecture

User Query
↓
FastAPI Endpoint
↓
Conversation Understanding
↓
Semantic Retrieval (FAISS)
↓
Boosting & Ranking Logic
↓
JSON Recommendation Response

---

# Features

## 1. Conversational Recommendation Engine

Supports:
- role-based recommendations
- follow-up refinements
- multi-turn interactions

Example:
- “Need leadership assessments”
- “CXOs with 15 years experience”
- “Add cognitive assessment”

---

## 2. Semantic Search

The system uses:
- sentence-transformers embeddings
- FAISS vector search

This allows retrieval based on meaning instead of exact keyword matching.

---

## 3. Clarification Questions

The system intelligently asks follow-up questions for vague queries.

Example:
- “Need leadership solution”
→ asks for role/seniority clarification

---

## 4. Refinement Support

Supports:
- add cognitive tests
- add simulations
- remove OPQ
- add situational judgement

without restarting the conversation.

---

## 5. Comparison Mode

Supports grounded comparison between assessments.

Example:
- “Compare OPQ Leadership Report and OPQ32r”

---

## 6. Safety & Refusal Handling 

The system avoids:
- legal advice
- hiring decision advice
- compliance interpretation

while still helping with assessment recommendations.

---

# Folder Structure

```text
SHL-AI_Agent/
│
├── app.py
├── retriever.py
├── catalog.json
├── requirements.txt
├── README.md
├── venv/

##. ENVIRONMENT SETUP-
Step 1 — Open Command Prompt

Navigate to project folder:

cd D:\SHL-AI_Agent
Step 2 — Create Virtual Environment
python -m venv venv
Step 3 — Activate Virtual Environment

Windows:
venv\Scripts\activate.bat

After activation:
(venv) appears in terminal.

Install required libraries:
pip install fastapi uvicorn requests beautifulsoup4 sentence-transformers faiss-cpu python-dotenv pydantic

Package	Purpose
fastapi       	Backend API
uvicorn	        Runs FastAPI server
requests	      HTTP requests
beautifulsoup4	HTML parsing
sentence-transformers	Embedding generation
faiss-cpu	Vector       similarity search
python-dotenv	         Environment variables
pydantic	             Request validation


##. CATALOG PREPARATION

The SHL catalog data is stored inside:

catalog.json

This file contains:

assessment names
duration
URLs
test type
remote support
adaptive support
descriptions

##. RETRIEVER SYSTEM

File: retriever.py

Responsibilities:

load catalog
create embeddings
build FAISS index
semantic retrieval
ranking improvements
Embedding Model

Used model:

all-MiniLM-L6-v2
from Sentence Transformers.
FAISS Vector Search
FAISS stores vector embeddings for fast similarity search.

Workflow:

Convert catalog descriptions into embeddings
Store vectors in FAISS index
Convert user query into embedding
Retrieve nearest matching assessments
Ranking Improvements
Custom boosting logic improves retrieval quality.

Examples:

leadership → OPQ boost
graduate → Graduate Scenarios boost
safety → DSI boost
healthcare → HIPAA boost

FastAPI Backend

File: app.py

Responsibilities:

API endpoints
multi-turn conversation handling
clarification logic
comparison logic
refinement logic
safety refusals
API Endpoints
Health Endpoint

GET /health:

Response:

{
  "status": "ok"
}
Chat Endpoint


POST /chat:

Request format:

{
  "messages": [
    {
      "role": "user",
      "content": "Need leadership assessments"
    }
  ]
}
Example Response
{
  "reply": "Recommended assessments: OPQ32r, OPQ Leadership Report",
  "recommendations": [
    {
      "name": "Occupational Personality Questionnaire OPQ32r",
      "url": "https://www.shl.com/",
      "duration": "25 minutes"
    }
  ],
  "end_of_conversation": false
}
Phase 6 — Running the Application

Start server:
uvicorn app:app --reload

Server runs on:
http://127.0.0.1:8000

Swagger UI:

http://127.0.0.1:8000/docs
{{{Testing}}}

The system was tested against:

leadership hiring
graduate hiring
Rust engineering
healthcare admin
contact center
safety-critical industrial roles
Excel/Word admin hiring
including multi-turn refinement conversations.

Name - Adurthi Mahathi Chinmayee
