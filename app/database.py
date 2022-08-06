from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from urllib.parse import quote  
from sqlalchemy.engine import create_engine
from .config import settings

SQLALCHEMY_DATABASE_URL = f'postgresql://postgres:Siddhu8897@localhost:5432/shiv'
#postgresql://<username>:<password>@<ip-address/hostname>/<database_name>

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

#dependencies #connection to database
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()