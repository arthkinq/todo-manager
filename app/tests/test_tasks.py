import pytest
from httpx import AsyncClient


async def create_user_and_get_token(client: AsyncClient, email: str, password: str) -> str:
    await client.post("/auth/register", json={"email": email, "password": password})
    response = await client.post("/auth/login", data={"username": email, "password": password})
    return response.json()["access_token"]


@pytest.mark.asyncio
async def test_create_task(client: AsyncClient):
    token = await create_user_and_get_token(client, "user1@test.com", "pass")
    headers = {"Authorization": f"Bearer {token}"}

    response = await client.post(
        "/api/v1/tasks",
        json={"title": "My first task", "description": "Doing something"},
        headers=headers
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "My first task"
    assert data["completed"] is False
    assert "id" in data
    assert "owner_id" in data


@pytest.mark.asyncio
async def test_get_own_tasks_only(client: AsyncClient):
    token1 = await create_user_and_get_token(client, "user1@test.com", "pass")
    headers1 = {"Authorization": f"Bearer {token1}"}
    await client.post("/api/v1/tasks", json={"title": "Task User 1"}, headers=headers1)

    token2 = await create_user_and_get_token(client, "user2@test.com", "pass")
    headers2 = {"Authorization": f"Bearer {token2}"}
    await client.post("/api/v1/tasks", json={"title": "Task User 2"}, headers=headers2)

    response = await client.get("/api/v1/tasks", headers=headers1)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["title"] == "Task User 1"


@pytest.mark.asyncio
async def test_update_other_user_task_forbidden(client: AsyncClient):
    token1 = await create_user_and_get_token(client, "user1@test.com", "pass")
    headers1 = {"Authorization": f"Bearer {token1}"}
    resp_task = await client.post("/api/v1/tasks", json={"title": "Task User 1"}, headers=headers1)
    task_id = resp_task.json()["id"]

    token2 = await create_user_and_get_token(client, "user2@test.com", "pass")
    headers2 = {"Authorization": f"Bearer {token2}"}

    response = await client.put(
        f"/api/v1/tasks/{task_id}",
        json={"title": "Hacked"},
        headers=headers2
    )
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_delete_task(client: AsyncClient):
    token = await create_user_and_get_token(client, "user1@test.com", "pass")
    headers = {"Authorization": f"Bearer {token}"}

    resp_task = await client.post("/api/v1/tasks", json={"title": "Task to delete"}, headers=headers)
    task_id = resp_task.json()["id"]

    resp_del = await client.delete(f"/api/v1/tasks/{task_id}", headers=headers)
    assert resp_del.status_code == 204

    resp_get = await client.get("/api/v1/tasks", headers=headers)
    assert len(resp_get.json()) == 0
