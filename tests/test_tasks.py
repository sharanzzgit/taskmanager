def test_create_task(client, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = client.post("/tasks/",headers=headers,json={
        "title":"Test Task",
        "description": "Testing",
        "status":"pending",
        "priority":"low",
        "due_date":"2026-05-06",
    })

    assert response.status_code == 200
    assert response.json()["title"] == "Test Task"

def test_get_tasks(client, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = client.get("/tasks/",headers=headers)

    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_task(client, auth_token):
    headers ={"Authorization": f"Bearer {auth_token}"}
    response = client.get("/tasks/1",headers=headers)

    assert response.status_code == 200
    assert response.json()["title"] == "Test Task"

def test_update_task(client, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = client.put("/tasks/1", headers=headers, json={
        "title": "Updated Task"
    })
    assert response.status_code == 200
    assert response.json()["title"] == "Updated Task"

def test_delete_task(client, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = client.delete("/tasks/1", headers=headers)
    assert response.status_code == 200
    assert response.json()["Message"] == "Task Deleted successfully"

def test_get_deleted_task(client, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = client.get("/tasks/1", headers=headers)
    assert response.status_code == 404
