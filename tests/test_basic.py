def test_index_redirect(client):
    response = client.get("/")
    assert response.status_code == 302
    # The location might be http://localhost/auth/login depending on how it's built
    assert "/auth/login" in response.headers["Location"]

def test_auth_and_index(client):
    # Register
    response = client.post("/auth/register", data={
        "username": "testuser",
        "password": "password",
        "Re-password": "password",
        "age": 25,
        "gender": "male",
        "weight": 70,
        "height": 70
    }, follow_redirects=True)
    assert response.status_code == 200

    # Login
    response = client.post("/auth/login", data={
        "username": "testuser",
        "password": "password"
    }, follow_redirects=True)
    assert response.status_code == 200

    # Now index should work
    response = client.get("/")
    assert response.status_code == 200
    # Check for title block content or something from layout
    assert b"Burn-Fat" in response.data
