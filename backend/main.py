from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sqlalchemy as sa
from routers import users, transactions, savings, subscriptions
from db import engine

app = FastAPI()

app.include_router(users.router)
app.include_router(transactions.router)
app.include_router(savings.router)
app.include_router(subscriptions.router)

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

metadata = sa.MetaData()

def create_tables():
  metadata.create_all(bind=engine)

create_tables()