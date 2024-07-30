import pytest


@pytest.mark.asyncio
async def test_create_user(client):
    user_data = {
        "email": "lol2221ad@gmail.com",
        "password1": "SamplePass123/!",
        "password2": "SamplePass123/!"
    }
    response = await client.post("/users/", json=user_data)
    assert response.status_code == 201


@pytest.mark.asyncio
async def test_create_user_is_exist_email(client):
    user_data = {
        "email": "lol2221ad1@gmail.com",
        "password1": "SamplePass123/!",
        "password2": "SamplePass123/!"
    }
    user_data_same = {
        "email": "lol2221ad1@gmail.com",
        "password1": "SamplePass123/!",
        "password2": "SamplePass123/!"
    }
    response = await client.post("/users/", json=user_data)
    response = await client.post("/users/", json=user_data_same)
    assert response.status_code == 400
    assert response.json() == {"detail": "Email is already exists."}


@pytest.mark.asyncio
async def test_create_user_password_is_not_strong_enough(client):
    user_data = {
        "email": "lol22421ad@gmail.com",
        "password1": "SamplePass123",
        "password2": "SamplePass123"
    }
    response = await client.post("/users/", json=user_data)
    assert response.status_code == 400
    assert response.json() == {"detail": "Password is not strong enough"}


@pytest.mark.asyncio
async def test_create_user_password_dont_match(client):
    user_data = {
        "email": "lol22421ad@gmail.com",
        "password1": "SamplePass12/3",
        "password2": "SamplePass12/13"
    }
    response = await client.post("/users/", json=user_data)
    assert response.status_code == 400
    assert response.json() == {"detail": "The password don't match"}


@pytest.mark.asyncio
async def test_get_user_by_id(client):
    response = await client.get("/users/1/")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_user_by_id_not_found(client):
    response = await client.get("/users/111/")
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}


@pytest.mark.asyncio
async def test_get_all_users(client):
    response = await client.get("/users/all")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_all_users_not_found(client):
    response = await client.get("/users/all?limit=3&offset=163")
    assert response.status_code == 404
    assert response.json() == {"detail": "Users do not exist"}


@pytest.mark.asyncio
async def test_update_user(client):
    user_data={
        "first_name": "string",
        "last_name": "string",
        "city": "string",
        "phone": "string",
        "avatar": "string",
    }
    response = await client.put("/users/1", json=user_data)
    assert response.status_code == 200
    data_resp = response.json()
    assert data_resp["user"]["first_name"] == "string"


@pytest.mark.asyncio
async def test_update_user_not_found(client):
    user_data={
        "first_name": "string",
        "last_name": "string",
        "city": "string",
        "phone": "string",
        "avatar": "string",
    }
    response = await client.put("/users/112", json=user_data)
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}


@pytest.mark.asyncio
async def test_delete_user(client):
    response = await client.delete("/users/1")
    assert response.status_code == 200
    assert response.json == {"message": "User deleted"}


@pytest.mark.asyncio
async def test_delete_user(client):
    response = await client.delete("/users/111")
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}