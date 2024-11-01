from fastapi import status


def test_registration_ok(client, fill_db):
    user = {"first_name": "Volodymyr",
            "last_name": "Kovalchuk",
            "email": "testMail@example.com",
            "password": "testpassword"}

    response = client.post("/auth/register", json=user)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == {'msg': 'User created successfully'}


def test_registration_existing_email(client, fill_db):
    user = {"first_name": "Oleksandr",
            "last_name": "Shevchenko",
            "email": "user2@mail.com",
            "password": "mypassword123"}

    response = client.post("/auth/register", json=user)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json().get("detail") == "User with this email already exists"


def test_registration_missing_field(client, fill_db):
    user = {"first_name": "Volodymyr",
            "email": "someMail5@mail.com",
            "password": "testpassword"}

    response = client.post("/auth/register", json=user)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_registration_empty_field(client, fill_db):
    user = {"first_name": "",
            "last_name": "",
            "email": "ffffaa@ukr.net",
            "password": "testpassword"}

    response = client.post("/auth/register", json=user)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert "This field cannot be empty" in response.json().get("detail")[0].get("msg")
    assert "This field cannot be empty" in response.json().get("detail")[1].get("msg")


def test_registration_invalid_email(client, fill_db):
    user = {"first_name": "Volodymyr",
            "last_name": "Kovalchuk",
            "email": "testMail",
            "password": "testpassword"}

    response = client.post("/auth/register", json=user)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert "value is not a valid email address" in response.json().get("detail")[0].get("msg")


def test_authorization(client, fill_db, test_user):
    response = client.post("/auth/login",
                           data={"username": test_user.email, "password": test_user.password})
    assert response.status_code == status.HTTP_200_OK
    assert response.json().get("access_token")
    assert response.json().get("token_type") == "bearer"


def test_authorization_invalid_credentials(client, fill_db):
    response = client.post("/auth/login",
                           data={"username": "fake@mail.com", "password": "fakepassword"})

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json().get("detail") == "Could not validate credentials"



