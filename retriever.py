import json
import faiss
import numpy as np

from sentence_transformers import SentenceTransformer

# Load model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Load catalog
with open("catalog.json", "r", encoding="utf-8") as f:
    catalog = json.load(f)

# Convert each assessment into searchable text
documents = []

for item in catalog:

    text = f"""
    Name: {item.get('name', '')}
    Description: {item.get('description', '')}
    Test Type: {item.get('test_type', '')}
    Remote Testing: {item.get('remote_testing', '')}
    Adaptive/IRT: {item.get('adaptive_irt', '')}
    Duration: {item.get('duration', '')}
    Job Levels: {item.get('job_levels', '')}
    Languages: {item.get('languages', '')}
    """

    documents.append(text)

# Create embeddings
embeddings = model.encode(documents)

# Convert to numpy array
embeddings = np.array(embeddings).astype("float32")

# Build FAISS index
dimension = embeddings.shape[1]

index = faiss.IndexFlatL2(dimension)
index.add(embeddings)

print(f"Loaded {len(catalog)} assessments into FAISS.")

# Search function
def search_assessments(query, top_k=5):

    query_embedding = model.encode([query])
    query_embedding = np.array(query_embedding).astype("float32")

    distances, indices = index.search(query_embedding, top_k)

    results = []

    for idx in indices[0]:
        results.append(catalog[idx])

    boosted_results = boost_results(query, results)

    return boosted_results


# Test search
if __name__ == "__main__":

    query = "Java backend developer with AWS and Docker"

    results = search_assessments(query)

    print("\nTop Matches:\n")

    for i, item in enumerate(results, 1):

        print(f"{i}. {item.get('name')}")
        print(item)
        print()
def boost_results(query, results):

    query_lower = query.lower()

    boosted = []

    for item in results:

        score = 0

        name = item.get("name", "").lower()

        # -----------------------------------
        # LEADERSHIP / EXECUTIVE ROLES
        # -----------------------------------

        if (
            "leadership" in query_lower
            or "director" in query_lower
            or "cxo" in query_lower
            or "executive" in query_lower
        ):

            if "opq32r" in name:
                score += 15

            if "opq" in name:
                score += 10

            if "leadership" in name:
                score += 8

            if "enterprise leadership" in name:
                score += 6

            if "hipo" in name:
                score += 4

        # -----------------------------------
        # GRADUATE / ENTRY LEVEL
        # -----------------------------------

        if (
            "graduate" in query_lower
            or "entry-level" in query_lower
            or "fresher" in query_lower
            or "trainee" in query_lower
        ):

            if "graduate scenarios" in name:
                score += 12

            if "verify" in name:
                score += 8

            if "numerical" in name:
                score += 6

        # -----------------------------------
        # SAFETY / INDUSTRIAL
        # -----------------------------------

        if (
            "safety" in query_lower
            or "chemical" in query_lower
            or "plant" in query_lower
            or "industrial" in query_lower
        ):

            if "dsi" in name:
                score += 12

            if "safety" in name:
                score += 10

            if "dependability" in name:
                score += 8

        # -----------------------------------
        # CUSTOMER SERVICE / CONTACT CENTER
        # -----------------------------------

        if (
            "contact center" in query_lower
            or "customer service" in query_lower
            or "call center" in query_lower
        ):

            if "svar" in name:
                score += 10

            if "simulation" in name:
                score += 8

            if "customer service" in name:
                score += 6

        # -----------------------------------
        # SOFTWARE / TECH
        # -----------------------------------

        if (
            "developer" in query_lower
            or "engineer" in query_lower
            or "backend" in query_lower
            or "software" in query_lower
        ):

            if "java" in name:
                score += 6

            if "aws" in name:
                score += 6

            if "docker" in name:
                score += 6

            if "linux" in name:
                score += 5

            if "network" in name:
                score += 4

            if "verify" in name:
                score += 3

        # -----------------------------------
        # ADMIN / OFFICE
        # -----------------------------------

        if (
            "admin" in query_lower
            or "assistant" in query_lower
            or "excel" in query_lower
            or "word" in query_lower
        ):

            if "excel" in name:
                score += 10

            if "word" in name:
                score += 10

            if "365" in name:
                score += 6

        boosted.append((score, item))

    # -----------------------------------
    # FORCE INCLUDE IMPORTANT ASSESSMENTS
    # -----------------------------------

    # Leadership roles -> OPQ32r
    if (
        "leadership" in query_lower
        or "director" in query_lower
        or "cxo" in query_lower
    ):

        already_exists = any(
            "opq32r" in item.get("name", "").lower()
            for score, item in boosted
        )

        if not already_exists:

            for item in catalog:

                if "opq32r" in item.get("name", "").lower():

                    boosted.append((20, item))
                    break

    # Graduate hiring -> Graduate Scenarios
    if "graduate" in query_lower:

        already_exists = any(
            "graduate scenarios" in item.get("name", "").lower()
            for score, item in boosted
        )

        if not already_exists:

            for item in catalog:

                if "graduate scenarios" in item.get("name", "").lower():

                    boosted.append((20, item))
                    break

    # -----------------------------------
    # SORT RESULTS
    # -----------------------------------

    boosted.sort(key=lambda x: x[0], reverse=True)

    # Remove duplicates
    final_results = []
    seen = set()

    for score, item in boosted:

        name = item.get("name")

        if name not in seen:

            final_results.append(item)
            seen.add(name)

    return final_results[:5]