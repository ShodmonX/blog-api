def test_create_user(client, test_user):
    res = client.post("/users/", json={
        "email": "new@example.com", "username": "newuser", "password": "newpass"
    })
    assert res.status_code == 200

    res_dup = client.post("/users/", json={
        "email": "new@example.com", "username": "another", "password": "pass"
    })
    assert res_dup.status_code == 400
    assert res_dup.json()["detail"] == "Email already registered"

    res_bad = client.post("/users/", json={"username": "x", "password": "y"})
    assert res_bad.status_code == 422
    assert res_bad.json()["detail"][0]["msg"] == "value is not a valid email address"



