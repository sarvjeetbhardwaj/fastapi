from fastapi.testclient import TestClient
from app.main import app
from app.schema import *
from app.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.database import get_db
from app.database import BASE
import pytest
from alembic import command


username = 'postgres'
password = r"Tuktuk123" 
hostname = r'localhost'
database_name = 'fastapi_test'


SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{password}@{hostname}/{database_name}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

testsessionlocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)

client =TestClient(app)

@pytest.fixture()
def session():
    BASE.metadata.drop_all(bind=engine)
    BASE.metadata.create_all(bind=engine)
    db = testsessionlocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    

    ## incase we want to use alembic to create and destroy table, use the following code
    #command.upgrade('head')
    #yield TestClient(app)
    #command.downgrade('base')