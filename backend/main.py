from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker, Session
from typing import List
import schemas
from models import users, transactions, expense_category

app = FastAPI()

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

db_url = f"mysql+pymysql://{"root"}:@{"localhost"}:{"3306"}/{"pennytracker"}"
engine = sa.create_engine(db_url, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
metadata = sa.MetaData()

def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()

def create_tables():
  metadata.create_all(bind=engine)

create_tables()

# ----- USERS -----

@app.get("/users/", response_model=List[schemas.User])
def get_all_users(db: Session = Depends(get_db)):
  query = sa.select(users)
  result = db.execute(query)
  rows = result.all()
  return [dict(row._mapping) for row in rows]

# ----- CATEGORIES -----

@app.get("/transactions/expense_categories/", response_model=List[schemas.ExpenseCategory])
def get_expense_categories(db: Session = Depends(get_db)):
  query = sa.select(expense_category)
  result = db.execute(query)
  rows = result.all()
  return [dict(row._mapping) for row in rows]

# ----- TRANSACTIONS -----

@app.get("/transactions/fetch_recent/", response_model=List[schemas.Transaction])
def get_recent_transactions(db: Session = Depends(get_db)):
  query = sa.select(
    transactions,
    expense_category.c.name.label("category_name")
  ).join(
    expense_category,
    transactions.c.category == expense_category.c.id
  ).order_by(
    transactions.c.date.desc()
  ).limit(6)

  result = db.execute(query)
  rows = result.all()
  return [dict(row._mapping) for row in rows]

@app.post("/transactions/new_expenditure/")
def post_new_expenditure(transaction_data: schemas.NewTransaction, db: Session = Depends(get_db)):
  query = sa.insert(transactions).values(**transaction_data.model_dump())
  db.execute(query)
  db.commit()
