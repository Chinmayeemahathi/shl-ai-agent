# SHL AI Recommendation System

---
title: SHL AI Agent
emoji: 🤖
colorFrom: blue
colorTo: indigo
sdk: docker
app_file: app.py
pinned: false
---

## 📌 Overview
This project is a conversational AI-powered recommendation system built for the SHL AI Internship Assignment.

The system recommends relevant SHL assessments based on:
- Job role
- Seniority
- Hiring requirements
- Follow-up refinements
- Conversational context

The project supports:
- Semantic search
- Multi-turn conversations
- Clarification questions
- Assessment comparisons
- Refinement handling
- Grounded recommendations from the SHL catalog

---

# 🛠️ Tech Stack

| Technology | Purpose |
| :--- | :--- |
| Python | Core backend language |
| FastAPI | REST API framework |
| Uvicorn | ASGI server |
| FAISS | Vector similarity search |
| JSON | Catalog storage |
| Swagger UI | API testing |

---

# 🏗️ Project Architecture

User Query → FastAPI Endpoint → Conversation Understanding → Semantic Retrieval → Ranking & Boosting → JSON Response

---

# 🌟 Features

## 1. Conversational Recommendation Engine
Supports:
- Role-based recommendations
- Follow-up refinements
- Multi-turn conversations

Example:
- "Need leadership assessments"
- "CXOs with 15 years experience"
- "Add cognitive assessment"

---

## 2. Semantic Retrieval
Uses FAISS vector search with lightweight embeddings to retrieve conceptually relevant SHL assessments.

---

## 3. Clarification Questions
Handles vague hiring requests intelligently.

Example:
- "Need leadership solution"
→ asks for role/seniority clarification.

---

## 4. Dynamic Refinement Support
Supports:
- Add cognitive assessments
- Add situational judgement
- Add simulations
- Multi-turn refinement

---

## 5. Comparison Mode
Supports grounded catalog comparisons.

Example:
- "Compare OPQ Leadership Report and OPQ32r"

---

## 6. Safety Handling
The system avoids:
- legal advice
- compliance interpretation
- hiring-decision recommendations

while remaining grounded to the SHL catalog.

---

# 📂 Folder Structure

```text
SHL-AI_Agent/
│
├── app.py
├── retriever.py
├── catalog.json
├── requirements.txt
├── Dockerfile
└── README.md

⚙️ Environment Setup
Step 1: Create Virtual Environment
python -m venv venv
Step 2: Activate Virtual Environment
venv\Scripts\activate.bat
Step 3: Install Dependencies
pip install -r requirements.txt
🚀 Run Application
uvicorn app:app --reload

Local API:

http://127.0.0.1:8000

Swagger:

http://127.0.0.1:8000/docs
🧪 Testing Coverage

Validated against:

Leadership hiring
Graduate hiring
Rust engineering roles
Contact center roles
Healthcare administration
Safety-critical manufacturing
Admin assistant screening
