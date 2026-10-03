import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from App.models import Base

SQLALCHEMY_DATABASE_URL = 'sqlite:///:memory:'

@pytest.fixture(scope="function")
def db_session():

    engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    Base.metadata.create_all(bind=engine)

    session = TestingSessionLocal()

    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)