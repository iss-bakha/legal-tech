from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health():
    assert client.get("/api/health").json() == {"status": "ok"}


def test_templates_listed():
    data = client.get("/api/documents/templates").json()
    assert data[0]["type"] == "deposit_claim"


def test_chat_validates_input():
    assert client.post("/api/chat", json={"question": ""}).status_code == 422
