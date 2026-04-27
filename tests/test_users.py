def test_get_profile(client, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = client.get("/users/me", headers = headers)

    assert response.status_code == 200
    assert response.json()["username"] is not None

def test_update_profile(client, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = client.put("/users/me",headers=headers,json={
        "username": "testzz"
    })

    assert response.status_code==200
    assert response.json()["username"] == "testzz"
    