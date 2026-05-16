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

Name- Adurthi Mahathi Chinmayee
