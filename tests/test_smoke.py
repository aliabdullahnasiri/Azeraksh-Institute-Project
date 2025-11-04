def test_ping(client):
    resp = client.get("/api/ping")
    assert resp.status_code == 200
    assert resp.json == {"status": "ok"}
