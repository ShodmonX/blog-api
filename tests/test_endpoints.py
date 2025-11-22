import pytest
from httpx import AsyncClient

async def test_root(client: AsyncClient):
    response = await client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data

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
    user1 = await client.post("/auth/register", json={
        "email": "posttest@gmail.com",
        "username": "postuser",
        "password": "test123"
    })
    user2 = await client.post("/auth/register", json={
        "email": "posttest2@gmail.com",
        "username": "postuser2",
        "password": "test123"
    })
    login1 = await client.post("/auth/login", json={
        "email": "posttest@gmail.com",
        "password": "test123"
    })
    login2 = await client.post("/auth/login", json={
        "email": "posttest2@gmail.com",
        "password": "test123"
    })
    token = login1.json()["access_token"]
    token2 = login2.json()["access_token"]
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

    get_resp = await client.get(f"/posts/{post_data['id']}")
    assert get_resp.status_code == 200
    post = get_resp.json()
    assert post["title"] == "My first post"
    assert post["content"] == "Hello world!"
    assert post["owner_id"] > 0


    updated_post = await client.put(f"/posts/{post_data['id']}", json={
        "title": "Updated title",
        "content": "Updated content"
    }, headers={"Authorization": f"Bearer {token}"})

    assert updated_post.status_code == 200
    updated_post_data = updated_post.json()
    assert updated_post_data["title"] == "Updated title"
    assert updated_post_data["content"] == "Updated content"

    updated_post2 = await client.put(f"/posts/{post_data['id']}", json={
        "title": "Updated title",
        "content": "Updated content"
    }, headers={"Authorization": f"Bearer {token2}"})

    assert updated_post2.status_code == 403

    delete_resp = await client.delete(f"/posts/{post_data['id']}", headers={"Authorization": f"Bearer {token}"})
    assert delete_resp.status_code == 204

    get_resp = await client.get(f"/posts/{post_data['id']}")
    assert get_resp.status_code == 404

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

async def test_update_profile(client: AsyncClient):
    await client.post("/auth/register", json={
        "email": "update@test.com",
        "username": "oldname",
        "password": "123456"
    })
    login = await client.post("/auth/login", json={
        "email": "update@test.com",
        "password": "123456"
    })
    token = login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    update = await client.put("/users/me", json={"username": "yanginomi"}, headers=headers)
    assert update.status_code == 200
    assert update.json()["username"] == "yanginomi"

async def test_full_post_crud_flow(client: AsyncClient):
    await client.post("/auth/register", json={
        "email": "crud@test.com",
        "username": "cruduser",
        "password": "crudpass123"
    })
    login = await client.post("/auth/login", json={
        "email": "crud@test.com",
        "password": "crudpass123"
    })
    token = login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    create = await client.post("/posts/", json={"title": "Test", "content": "Hello"}, headers=headers)
    assert create.status_code == 201
    post_id = create.json()["id"]

    get = await client.get(f"/posts/{post_id}")
    assert get.status_code == 200
    assert get.json()["title"] == "Test"

    update = await client.put(f"/posts/{post_id}", json={"title": "Yangilandi!"}, headers=headers)
    assert update.status_code == 200
    assert update.json()["title"] == "Yangilandi!"

    delete = await client.delete(f"/posts/{post_id}", headers=headers)
    assert delete.status_code == 204

    not_found = await client.get(f"/posts/{post_id}")
    assert not_found.status_code == 404

async def test_refresh_and_logout(client: AsyncClient):
    await client.post("/auth/register", json={
        "email": "refresh@test.com",
        "username": "refuser",
        "password": "123456"
    })
    login = await client.post("/auth/login", json={
        "email": "refresh@test.com",
        "password": "123456"
    })

    refresh = await client.post("/auth/refresh")
    assert refresh.status_code == 401

    logout = await client.post("/auth/logout")
    assert logout.status_code == 200

    failed = await client.post("/auth/refresh")
    assert failed.status_code == 401