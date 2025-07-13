def test_create_post(client, test_user):
    # Login to get token
    res = client.post("/login", data={"username": test_user.email, "password": "test123"})
    token = res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Create post
    post_data = {"title": "Test post", "content": "Test content"}
    res = client.post("/posts/", json=post_data, headers=headers)

    assert res.status_code == 200
    data = res.json()
    assert data["title"] == "Test post"
    assert data["content"] == "Test content"
    assert "id" in data

    # Create another post
    post_data = {"title": "Test post 2", "content": "Test content 2"}
    res = client.post("/posts/", json=post_data, headers=headers)

    assert res.status_code == 200
    data = res.json()
    assert data["title"] == "Test post 2"
    assert data["content"] == "Test content 2"
    assert "id" in data

    # Get all posts
    res = client.get("/posts/", headers=headers)

    assert res.status_code == 200
    data = res.json()
    assert len(data) == 2

    # Get one post
    res = client.get(f"/posts/{data[0]['id']}", headers=headers)

    assert res.status_code == 200
    data = res.json()
    assert data["title"] == "Test post"
    assert data["content"] == "Test content"

    # Delete post
    res = client.delete(f"/posts/{data[0]['id']}", headers=headers)

    assert res.status_code == 204

    # Get all posts again
    res = client.get("/posts/", headers=headers)

    assert res.status_code == 200
    data = res.json()
    assert len(data) == 1

    # Get one post again (should be 404, since we deleted it)
    res = client.get(f"/posts/{data[0]['id']}", headers=headers)

    assert res.status_code == 404

    # Delete post again
    res = client.delete(f"/posts/{data[0]['id']}", headers=headers)

    assert res.status_code == 404