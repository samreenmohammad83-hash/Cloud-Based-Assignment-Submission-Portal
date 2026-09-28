from fastapi.testclient import TestClient
from backend.app.main import app

client=TestClient(app)

def test_health():
    r=client.get("/health"); assert r.status_code==200; assert r.json()["status"]=="ok"

def test_invalid_login():
    r=client.post("/api/login",json={"email":"nobody@example.com","password":"badpass"}); assert r.status_code==401
