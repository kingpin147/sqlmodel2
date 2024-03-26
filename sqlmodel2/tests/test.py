import requests
from fastapi.testclient import TestClient

from .main import app


# Define a test client using TestClient
client = TestClient(app)

# Define a function to test the create task endpoint
def test_create_task():
    url = "/task/"
    data = {"content": "Test task"}
    response = client.post(url, json=data)
    assert response.status_code == 200
    print("Create task test passed")

# Define a function to test the read tasks endpoint
def test_read_tasks():
    url = "/task/"
    response = client.get(url)
    assert response.status_code == 200
    print("Read tasks test passed")
    print("Tasks:", response.json())

# Define a function to test the update task endpoint
def test_update_task():
    # First, create a task to update
    create_response = client.post("/task/", json={"content": "Test task to update"})
    assert create_response.status_code == 200
    task_id = create_response.json()["id"]

    # Update the task
    update_response = client.put(f"/task/", json={"id": task_id, "content": "Updated test task"})
    assert update_response.status_code == 200
    print("Update task test passed")

# Define a function to test the delete task endpoint
def test_delete_task():
    # First, create a task to delete
    create_response = client.post("/task/", json={"content": "Test task to delete"})
    assert create_response.status_code == 200
    task_id = create_response.json()["id"]

    # Delete the task
    delete_response = client.delete(f"/task/?id={task_id}")
    assert delete_response.status_code == 200
    print("Delete task test passed")

# Run all the test functions
test_create_task()
test_read_tasks()
test_update_task()
test_delete_task()
