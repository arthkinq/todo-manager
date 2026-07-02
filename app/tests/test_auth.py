import pytest
from httpx import AsyncClient
from app.schemas.user import UserCreate


@pytest.mark.asyncio
async def test_register_user(client: AsyncClient):
    response = await client.post(
        "/auth/register",
        json={"email": "test@example.com", "password": "password123"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "test@example.com"
    assert "id" in data
    assert data["is_active"] is True


@pytest.mark.asyncio
async def test_register_duplicate_user(client: AsyncClient):
    await client.post(
        "/auth/register",
        json={"email": "test@example.com", "password": "password123"}
    )
    response = await client.post(
        "/auth/register",
        json={"email": "test@example.com", "password": "password456"}
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "User with this email already exists."


@pytest.mark.asyncio
async def test_login_success(client: AsyncClient):
    await client.post(
        "/auth/register",
        json={"email": "test@example.com", "password": "password123"}
    )
    response = await client.post(
        "/auth/login",
        data={"username": "test@example.com", "password": "password123"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_login_wrong_password(client: AsyncClient):
    await client.post(
        "/auth/register",
        json={"email": "test@example.com", "password": "password123"}
    )
    response = await client.post(
        "/auth/login",
        data={"username": "test@example.com", "password": "wrongpassword"}
    )
    assert response.status_code == 400
