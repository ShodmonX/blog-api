import pytest
from httpx import AsyncClient

async def test_root(client: AsyncClient):
    response = await client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert data["message"] == "Hello World"

async def test_register_success(client: AsyncClient):
    response = await client.post("/auth/register", json={
        "email": "test@gmail.com",
        "username": "testuser",
        "password": "testpass123"
    })
    
    assert response.status_code == 201
    
    data = response.json()
    assert "msg" in data
    assert data["msg"] == "User created"
    assert "user" in data
    user = data["user"]
    assert "email" in user
    assert user["email"] == "test@gmail.com"
    assert "username" in user
    assert user["username"] == "testuser"

    response_login = await client.post("/auth/login", json={
        "email": "test@gmail.com",
        "password": "testpass123"
    })

    assert response_login.status_code == 200
    data = response_login.json()
    assert "access_token" in data
    assert "token_type" in data
    assert data["token_type"] == "bearer"

    response_me = await client.get("/users/me", headers={
        "Authorization": f"Bearer {data['access_token']}"
    })

    assert response_me.status_code == 200
    user_data = response_me.json()
    assert "id" in user_data
    assert "email" in user_data
    assert "username" in user_data
    assert user_data["email"] == "test@gmail.com"
    assert user_data["username"] == "testuser"

async def test_register_fail(client: AsyncClient):
    response1 = await client.post("/auth/register", json={
        "email": "duplicate@gmail.com",
        "username": "user1", 
        "password": "testpass123"
    })
    assert response1.status_code == 201

    response2 = await client.post("/auth/register", json={
        "email": "duplicate@gmail.com",
        "username": "user2",
        "password": "testpass123" 
    })
    assert response2.status_code == 400
    assert response2.json()["detail"] == "User already exists with this email"

    response3 = await client.post("/auth/register", json={
        "email": "notduplicate@gmail.com",
        "username": "user1",
        "password": "testpass123"
    })
    assert response3.status_code == 400
    assert response3.json()["detail"] == "User already exists with this username"

    refresh_response = await client.post("/auth/refresh")
    assert refresh_response.status_code == 401

async def test_refresh_token_with_httponly_cookie(client: AsyncClient):
    await client.post("/auth/register", json={
        "email": "cookie@test.com",
        "username": "cookieman",
        "password": "cookietest123"
    })

    login_resp = await client.post("/auth/login", json={
        "email": "cookie@test.com",
        "password": "cookietest123"
    })
    assert login_resp.status_code == 200

    refresh_cookie = login_resp.cookies.get("refresh_token")
    assert refresh_cookie is not None

async def test_create_and_get_post(client: AsyncClient):
    await client.post("/auth/register", json={
        "email": "posttest@gmail.com",
        "username": "postuser",
        "password": "test123"
    })
    login = await client.post("/auth/login", json={
        "email": "posttest@gmail.com",
        "password": "test123"
    })
    token = login.json()["access_token"]
    create_resp = await client.post("/posts/", json={
        "title": "My first post",
        "content": "Hello world!"
    }, headers={"Authorization": f"Bearer {token}"})
    assert create_resp.status_code == 201
    post_data = create_resp.json()
    assert post_data["title"] == "My first post"
    assert post_data["owner_id"] > 0

    get_resp = await client.get("/posts/")
    assert get_resp.status_code == 200
    posts = get_resp.json()
    assert len(posts) >= 1
    assert any(p["title"] == "My first post" for p in posts)

async def test_logout(client: AsyncClient):
    response = await client.post("/auth/register", json={
        "email": "test@gmail.com",
        "username": "testuser",
        "password": "testpass123"
    })
    assert response.status_code == 201

    login_response = await client.post("/auth/login", json={
        "email": "test@gmail.com",
        "password": "testpass123"
    })
    assert login_response.status_code == 200

    logout_response = await client.post("/auth/logout", headers={
        "Authorization": f"Bearer {login_response.json()['access_token']}"
    })
    assert logout_response.status_code == 200