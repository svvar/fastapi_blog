from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool


from app.db.base import Base
from app.db.session import get_db
from app.main import app


DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False}, poolclass=StaticPool)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_testing_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_test_db():
    Base.metadata.create_all(bind=engine)


def teardown_test_db():
    Base.metadata.drop_all(bind=engine)


app.dependency_overrides[get_db] = get_testing_db


