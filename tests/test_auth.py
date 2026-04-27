
def test_register(client):
    response = client.post("/auth/register",json={
        "username":"testuser",
        "password":"test1234",
        "email":"test@test.com"
    })
    assert response.status_code == 200
    assert response.json()["username"] =="testuser"

def test_register_duplicate(client):
    response = client.post("/auth/register",json={
        "username": "testuser",
        "password": "test1234",
        "email": "test@test.com"
    })

    assert response.status_code == 400

def test_login(client):
    reponse = client.post("/auth/login",data={
        "username": "test@test.com",
        "password": "test1234"
    })

    assert reponse.status_code == 200
    assert reponse.json()["access_token"] is not None

def test_login_wrong_password(client):
    response = client.post("/auth/login",data={
        "username": "test@test.com",
        "password": "test"
    })

    assert response.status_code == 401