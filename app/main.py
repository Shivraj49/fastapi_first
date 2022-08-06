from fastapi import FastAPI
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from .import models
from .database import engine
from .routers import auth, post,user,vote
from .config import Settings
from fastapi.middleware.cors import CORSMiddleware  
from mangum import Mangum

models.Base.metadata.create_all(bind=engine)  #sqlalchemy
 
origins = ["*"]
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Connecting to the database using psycopg2
'''while True:
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres',
                                password='Siddhu@8897', cursor_factory=RealDictCursor)  # Setting up required field
        cursor = conn.cursor()
        print("Database Connection was Successful")
        break

    except Exception as error:
        print("Connection to database was failed")
        print("Error :", error)
        time.sleep(2)


my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1}, {
    "title": "Foods", "content": "Pizza", "id": 2}] 


def find_post(id):
    for p in my_posts:
        if p['id'] == id:
            return p

# ------------------------------------------------------------------------------------------------


def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i '''


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)
