def test_login_user(client, test_user):
    res = client.post("/login", data={"username": test_user.email, "password": "test123"})
    assert res.status_code == 200
    assert "access_token" in res.json()
    assert "token_type" in res.json()




