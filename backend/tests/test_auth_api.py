def test_register_and_login_flow(client):
    email = "alice@example.com"
    password = "StrongP@ss"
    # Register
    r = client.post("/auth/register", json={"email": email, "password": password, "role": "user"})
    assert r.status_code == 201, r.text
    data = r.json()
    assert data["email"] == email
    assert data["role"] == "user"
    assert "id" in data

    # Login
    r2 = client.post("/auth/login", json={"email": email, "password": password})
    assert r2.status_code == 200, r2.text
    token_payload = r2.json()
    assert "access_token" in token_payload
    assert token_payload["token_type"] == "bearer"