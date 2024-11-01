import random
from datetime import datetime

import pytest
from faker import Faker
from passlib.hash import bcrypt
from fastapi.testclient import TestClient

from app.main import app
from app.schemas.user import UserLogin
from app.db.models.user_model import User as UserDB
from app.db.models.post_model import Post as PostDB
from app.db.models.comment_model import Comment as CommentDB
from tests.db_setup import get_testing_db, init_test_db, teardown_test_db, TestingSessionLocal


@pytest.fixture(scope="module")
def get_test_db():
    init_test_db()
    yield get_testing_db()
    teardown_test_db()


@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="module")
def test_user(fill_db):
    yield UserLogin(email="testUser@mail.com", password="testpassword")


@pytest.fixture(scope="module")
def bearer_token(client, test_user):
    return (client.post("/auth/login",
                        data={"username": test_user.email, "password": test_user.password})
            .json().get("access_token"))


@pytest.fixture(scope="module")
def fill_db(get_test_db):
    users = [
        UserDB(id=0, email="testUser@mail.com", password=bcrypt.hash("testpassword"), first_name="Oleksandr", last_name="Shevchenko"),
        UserDB(id=1, email="user2@mail.com", password=bcrypt.hash("SECRET"), first_name="Katy", last_name="Perry"),
        UserDB(id=2, email="user3@mail.com", password=bcrypt.hash("SECRET"), first_name="Bebe", last_name="Rexha"),
    ]

    posts = [
        PostDB(id=0, content="Hello my first test post", owner_id=0, created_at=datetime(2024, 9, 2)),
        PostDB(id=1, content="This is second post I'll use", owner_id=0, created_at=datetime(2024, 9, 14)),
        PostDB(id=2, content="Well, I'm doing a test task now", owner_id=1, created_at=datetime(2024, 10, 2)),
        PostDB(id=3, content="It was pretty interesting", owner_id=1, created_at=datetime(2024, 10, 3)),
    ]

    comments_data = []

    # Some random fake comments
    faker = Faker()
    for i in range(50):
        reply_to_list = [None] * 33 + list(range(51))
        comments_data.append(CommentDB(id=i,
                                       content=faker.sentence(nb_words=10),
                                       post_id=random.choice([0, 1, 2, 3]),
                                       owner_id=random.choice([0, 1, 2]),
                                       created_at=faker.date_time_between(start_date=datetime(2024, 9, 1), end_date=datetime(2024, 9, 30)),
                                       is_blocked=random.choice([True, False, False, False, False]),
                                       reply_to=random.choice(reply_to_list))
                             )

    # Some comments to check statistics
    comments_data.extend([
        CommentDB(id=50, content=faker.sentence(nb_words=10), post_id=0, owner_id=1, created_at=datetime(2024, 10, 1), is_blocked=False),
        CommentDB(id=51, content=faker.sentence(nb_words=10), post_id=1, owner_id=2, created_at=datetime(2024, 10, 1), is_blocked=False),
        CommentDB(id=52, content=faker.sentence(nb_words=10), post_id=2, owner_id=2, created_at=datetime(2024, 10, 1), is_blocked=True),
        CommentDB(id=53, content=faker.sentence(nb_words=10), post_id=3, owner_id=0, created_at=datetime(2024, 10, 2), is_blocked=True),
        CommentDB(id=54, content=faker.sentence(nb_words=10), post_id=2, owner_id=1, created_at=datetime(2024, 10, 2), is_blocked=False),
        CommentDB(id=55, content=faker.sentence(nb_words=10), post_id=0, owner_id=1, created_at=datetime(2024, 10, 2), is_blocked=False),
        CommentDB(id=56, content=faker.sentence(nb_words=10), post_id=3, owner_id=2, created_at=datetime(2024, 10, 3), is_blocked=False),
        CommentDB(id=57, content=faker.sentence(nb_words=10), post_id=0, owner_id=2, created_at=datetime(2024, 10, 3), is_blocked=False),
        CommentDB(id=58, content=faker.sentence(nb_words=10), post_id=3, owner_id=2, created_at=datetime(2024, 10, 4), is_blocked=True),
        CommentDB(id=59, content=faker.sentence(nb_words=10), post_id=0, owner_id=0, created_at=datetime(2024, 10, 5), is_blocked=False),
        CommentDB(id=60, content=faker.sentence(nb_words=10), post_id=0, owner_id=0, created_at=datetime(2024, 10, 6), is_blocked=False),
        CommentDB(id=61, content=faker.sentence(nb_words=10), post_id=1, owner_id=1, created_at=datetime(2024, 10, 6), is_blocked=True),
        CommentDB(id=62, content=faker.sentence(nb_words=10), post_id=1, owner_id=2, created_at=datetime(2024, 10, 6), is_blocked=False),
        CommentDB(id=63, content=faker.sentence(nb_words=10), post_id=0, owner_id=1, created_at=datetime(2024, 10, 7), is_blocked=False),
        CommentDB(id=64, content=faker.sentence(nb_words=10), post_id=1, owner_id=2, created_at=datetime(2024, 10, 7), is_blocked=False),
        CommentDB(id=65, content=faker.sentence(nb_words=10), post_id=2, owner_id=1, created_at=datetime(2024, 10, 8), is_blocked=False),
        CommentDB(id=66, content=faker.sentence(nb_words=10), post_id=0, owner_id=2, created_at=datetime(2024, 10, 9), is_blocked=True),
    ])

    with TestingSessionLocal() as db:
        db.add_all(users)
        db.add_all(posts)
        db.add_all(comments_data)
        db.commit()

