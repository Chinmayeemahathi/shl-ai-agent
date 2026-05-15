from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

from retriever import search_assessments

app = FastAPI(
    title="SHL AI Recommendation API",
    version="1.0"
)


# -----------------------------------
# Request Models
# -----------------------------------

class Message(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    messages: List[Message]


# -----------------------------------
# Health Endpoint
# -----------------------------------

@app.get("/health")
def health():
    return {
        "status": "ok"
    }


# -----------------------------------
# Chat Endpoint
# -----------------------------------

@app.post("/chat")
def chat(req: ChatRequest):

    
    latest_message = req.messages[-1].content

# Combine all user messages into context
    conversation_context = " ".join(
        [
            msg.content
            for msg in req.messages
            if msg.role == "user"
        ]
    )   

    latest_message_lower = latest_message.lower().strip()
    

    # -----------------------------------
    # END CONVERSATION DETECTION
    # -----------------------------------

    completion_phrases = [
        "thanks",
        "thank you",
        "perfect",
        "confirmed",
        "that works",
        "looks good",
        "great",
        "done"
    ]

    if latest_message_lower in completion_phrases:

        return {
            "reply": "Glad I could help. Final shortlist confirmed.",
            "recommendations": [],
            "end_of_conversation": True
        }

    # -----------------------------------
    # CLARIFICATION LOGIC
    # -----------------------------------

    vague_queries = [
        "leadership solution",
        "need hiring solution",
        "need assessment",
        "need assessments"
    ]

    if (
        latest_message_lower in vague_queries
        or len(latest_message_lower.split()) <= 3
    ):

        return {
            "reply": "Could you share more about the role, seniority level, or specific skills you're hiring for?",
            "recommendations": [],
            "end_of_conversation": False
        }

    # -----------------------------------
    # NORMAL RETRIEVAL
    # -----------------------------------

    results = search_assessments(conversation_context, top_k=5)

    recommendations = []

    for item in results:

        recommendations.append({
            "name": item.get("name"),
            "url": item.get("link"),
            "test_type": item.get("keys"),
            "duration": item.get("duration"),
            "remote_testing": item.get("remote"),
            "adaptive_support": item.get("adaptive")
        })

    return {
        "reply": f"Here are recommended assessments for: {latest_message}",
        "recommendations": recommendations,
        "end_of_conversation": False
    }