from fastapi.testclient import TestClient


ANALYZE_PAYLOAD = {
    "text": "New semiconductor export controls affect advanced chip supply chains and market access.",
    "language": "en",
    "output_mode": "analyst",
    "question_text": "What should determine this decision?",
}


def create_analysis_run(client: TestClient) -> dict:
    response = client.post("/analyze", json=ANALYZE_PAYLOAD)
    assert response.status_code == 200
    return response.json()
