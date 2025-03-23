from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from .config import settings


username = 'postgres'
password = r"Tuktuk123" 
hostname = r'localhost'
database_name = 'fastapi'

SQLALCHEMY_DATABASE_URL = f'postgresql://{username}:{password}@{hostname}:5432/{database_name}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

sessionlocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)

BASE = declarative_base()

def get_db():
    db = sessionlocal()
    try:
        yield db
    finally:
        db.close()


# below code can be used when we are using raw sql code 
'''
while True:
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password = 'Tuktuk123',
                                cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print('Database connection was successful')
        break
    except Exception as error:
        print('connection to database failed')
        print('Error', error)
        time.sleep(2)
'''