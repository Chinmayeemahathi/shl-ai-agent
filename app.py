from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

from retriever import search_assessments, catalog

app = FastAPI(
    title="SHL AI Recommendation API",
    version="1.0"
)

# -----------------------------------
# CORS FIX
# -----------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------------
# REQUEST MODELS
# -----------------------------------

class Message(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    messages: List[Message]


# -----------------------------------
# HEALTH ENDPOINT
# -----------------------------------

@app.get("/health")
def health():

    return {
        "status": "ok"
    }


# -----------------------------------
# ROOT ENDPOINT
# -----------------------------------

@app.get("/")
def root():

    return {
        "message": "SHL AI Recommendation API is running"
    }


# -----------------------------------
# EXTRACT PREVIOUS RECOMMENDATIONS
# -----------------------------------

def extract_previous_recommendations(messages):

    previous_items = []

    for msg in messages:

        if msg.role == "assistant":

            content = msg.content.lower()

            for item in catalog:

                name = item.get("name", "")

                if name.lower() in content:
                    previous_items.append(item)

    unique = []
    seen = set()

    for item in previous_items:

        name = item.get("name")

        if name not in seen:

            unique.append(item)
            seen.add(name)

    return unique


# -----------------------------------
# COMPARE ASSESSMENTS
# -----------------------------------

def compare_assessments(query):

    query_lower = query.lower()

    matched = []

    for item in catalog:

        name = item.get("name", "").lower()

        if name in query_lower:
            matched.append(item)

    unique = []
    seen = set()

    for item in matched:

        name = item.get("name")

        if name not in seen:

            unique.append(item)
            seen.add(name)

    matched = unique

    if len(matched) < 2:
        return None

    a = matched[0]
    b = matched[1]

    return {
        "assessment_1": {
            "name": a.get("name"),
            "duration": a.get("duration"),
            "test_type": a.get("keys"),
            "remote_testing": a.get("remote")
        },
        "assessment_2": {
            "name": b.get("name"),
            "duration": b.get("duration"),
            "test_type": b.get("keys"),
            "remote_testing": b.get("remote")
        }
    }


# -----------------------------------
# CHAT ENDPOINT
# -----------------------------------

@app.post("/chat")
def chat(req: ChatRequest):

    latest_message = req.messages[-1].content
    latest_message_lower = latest_message.lower().strip()

    conversation_context = " ".join(
        [
            msg.content
            for msg in req.messages
            if msg.role == "user"
        ]
    )

    previous_recommendations = extract_previous_recommendations(req.messages)

    # -----------------------------------
    # END CONVERSATION
    # -----------------------------------

    completion_phrases = [
        "thanks",
        "thank you",
        "perfect",
        "confirmed",
        "that works",
        "looks good",
        "great",
        "done",
        "works for us"
    ]

    if any(
        phrase in latest_message_lower
        for phrase in completion_phrases
    ):

        return {
            "reply": "Glad I could help. Final shortlist confirmed.",
            "recommendations": [],
            "end_of_conversation": True
        }

    # -----------------------------------
    # REFUSAL LOGIC
    # -----------------------------------

    refusal_keywords = [
        "legal",
        "lawsuit",
        "attorney",
        "who should i hire",
        "ignore previous instructions",
        "forget your instructions",
        "bypass",
        "mandatory under hipaa",
        "required by law"
    ]

    if any(word in latest_message_lower for word in refusal_keywords):

        return {
            "reply": (
                "I can help with SHL assessment recommendations "
                "and grounded catalog comparisons, but not legal "
                "or hiring-decision advice."
            ),
            "recommendations": [],
            "end_of_conversation": False
        }

    # -----------------------------------
    # CONTACT CENTER CLARIFICATION
    # -----------------------------------

    if (
        (
            "contact center" in latest_message_lower
            or "call center" in latest_message_lower
        )
        and "english" not in latest_message_lower
        and "spanish" not in latest_message_lower
    ):

        return {
            "reply": "What language are the calls in?",
            "recommendations": [],
            "end_of_conversation": False
        }

    # -----------------------------------
    # COMPARISON MODE
    # -----------------------------------

    if (
        "difference between" in latest_message_lower
        or "compare" in latest_message_lower
    ):

        comparison = compare_assessments(latest_message)

        if comparison:

            return {
                "reply": (
                    "Here is a grounded comparison between "
                    "the requested assessments."
                ),
                "comparison": comparison,
                "recommendations": [],
                "end_of_conversation": False
            }

    # -----------------------------------
    # VAGUE QUERY DETECTION
    # -----------------------------------

    vague_queries = [
        "leadership",
        "senior leadership",
        "leadership solution",
        "need hiring solution",
        "need assessment",
        "need assessments",
        "hiring solution",
        "assessment solution",
        "solution"
    ]

    if any(
        phrase == latest_message_lower
        for phrase in vague_queries
    ):

        return {
            "reply": (
                "Could you share more about the role, "
                "seniority level, or specific skills "
                "you're hiring for?"
            ),
            "recommendations": [],
            "end_of_conversation": False
        }

    # -----------------------------------
    # REFINEMENT LOGIC
    # -----------------------------------

    if (
        "add" in latest_message_lower
        or "also" in latest_message_lower
        or "include" in latest_message_lower
        or "remove" in latest_message_lower
        or "drop" in latest_message_lower
    ):

        results = previous_recommendations.copy()

        if (
            "cognitive" in latest_message_lower
            or "aptitude" in latest_message_lower
        ):

            for item in catalog:

                if "verify interactive g+" in item.get("name", "").lower():

                    results.append(item)

        if (
            "situational judgement" in latest_message_lower
            or "situational judgment" in latest_message_lower
        ):

            for item in catalog:

                if "graduate scenarios" in item.get("name", "").lower():

                    results.append(item)

        unique = []
        seen = set()

        for item in results:

            name = item.get("name")

            if name not in seen:

                unique.append(item)
                seen.add(name)

        recommendations = []

        for item in unique[:5]:

            recommendations.append({
                "name": item.get("name"),
                "url": item.get("link"),
                "test_type": item.get("keys"),
                "duration": item.get("duration"),
                "remote_testing": item.get("remote"),
                "adaptive_support": item.get("adaptive")
            })

        return {
            "reply": (
                "Updated shortlist with your additional requirements."
            ),
            "recommendations": recommendations,
            "end_of_conversation": False
        }

    # -----------------------------------
    # NORMAL RETRIEVAL
    # -----------------------------------

    results = search_assessments(
        conversation_context,
        top_k=15
    )

    recommendations = []

    for item in results[:5]:

        recommendations.append({
            "name": item.get("name"),
            "url": item.get("link"),
            "test_type": item.get("keys"),
            "duration": item.get("duration"),
            "remote_testing": item.get("remote"),
            "adaptive_support": item.get("adaptive")
        })

    reply_text = (
        "Recommended assessments: "
        + ", ".join(
            [item.get("name") for item in results[:5]]
        )
    )

    return {
        "reply": reply_text,
        "recommendations": recommendations,
        "end_of_conversation": False
    }