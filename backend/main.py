from fastapi import FastAPI, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker, Session
from typing import List
import schemas
from models import users, transactions, expense_category, subscriptions

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

#fetch recent transactions, ordered by date
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

#fetch all transactions
@app.get("/transactions/fetch_all/", response_model=List[schemas.Transaction])
def get_all_transactions(db: Session = Depends(get_db)):
  query = sa.select(
    transactions,
    expense_category.c.name.label("category_name")
  ).join(
    expense_category,
    transactions.c.category == expense_category.c.id
  ).order_by(
    transactions.c.date.desc()
  )
  result = db.execute(query)
  rows = result.all()
  return [dict(row._mapping) for row in rows]

#insert new transaction
@app.post("/transactions/new_expenditure/")
def post_new_expenditure(transaction_data: schemas.NewTransaction, db: Session = Depends(get_db)):
  query = sa.insert(transactions).values(**transaction_data.model_dump())
  db.execute(query)
  db.commit()

#fetch data summarized for categories filtered by month
@app.get("/transactions/fetch_by_category")
def fetch_by_category(db: Session = Depends(get_db), user_id: int = Query(), month: str = Query()):
  date_pattern = f"%-{month}-%"

  query = sa.select(
    expense_category.c.name,
    transactions.c.method,
    sa.func.sum(transactions.c.amount)
  ).join(
    transactions,
    transactions.c.category == expense_category.c.id
  ).where(
    transactions.c.user_id == user_id,
    transactions.c.date.like(date_pattern)
  ).group_by(
    expense_category.c.name,
    transactions.c.method
  )
  
  result = db.execute(query)
  rows = result.all()
  
  categories = {}

  for row in rows:
    category, method, amount = row[0], row[1], row[2]

    if category not in categories:
        categories[category] = { "total": 0.0, "method": {} }

    categories[category]["total"] += amount
    categories[category]["method"][method] = amount

  expenses = []
  for category, data in categories.items():
    expenses.append(
      {
          "category": category,
          "total": data["total"],
          "method": data["method"]
      }
    )

  total_query = sa.select(
    sa.func.sum(transactions.c.amount)
  ).where(
    transactions.c.user_id == user_id,
    transactions.c.date.like(date_pattern)
  )

  total_result = db.execute(total_query).scalar_one_or_none() 

  return { "expenses": expenses, "total": total_result}

#fetch data summarized for method filtered by month
@app.get("/transactions/fetch_by_method")
def fetch_by_method(db: Session = Depends(get_db), user_id: int = Query(), month: str = Query()):
  date_pattern = f"%-{month}-%"

  query = sa.select(
    expense_category.c.name,
    transactions.c.method,
    sa.func.sum(transactions.c.amount)
  ).join(
    transactions,
    transactions.c.category == expense_category.c.id
  ).where(
    transactions.c.user_id == user_id,
    transactions.c.date.like(date_pattern)
  ).group_by(
    expense_category.c.name,
    transactions.c.method
  )
  
  result = db.execute(query)
  rows = result.all()
  
  methods = {}

  for row in rows:
    category, method, amount = row[0], row[1], row[2]

    if method not in methods:
        methods[method] = { "total": 0.0, "categories": {} }

    methods[method]["total"] += amount
    methods[method]["categories"][category] = amount

  expenses = []
  for methods, data in methods.items():
    expenses.append(
      {
          "method": methods,
          "total": data["total"],
          "category": data["categories"]
      }
    )

  total_query = sa.select(
    sa.func.sum(transactions.c.amount)
  ).where(
    transactions.c.user_id == user_id,
    transactions.c.date.like(date_pattern)
  )

  total_result = db.execute(total_query).scalar_one_or_none() 

  return { "expenses": expenses, "total": total_result}

# ----- SUBSCRIPTIONS -----

#fetch all subscriptions
@app.get("/subscriptions/fetch_all/", response_model=List[schemas.Subscription])
def get_all_subscriptions(db: Session = Depends(get_db)):
  query = sa.select(
    subscriptions
  ).order_by(
    subscriptions.c.start_date.asc()
  )

  result = db.execute(query)
  rows = result.all()
  return [dict(row._mapping) for row in rows]

#insert new subscription
@app.post("/subscriptions/new_subscription/")
def post_new_subscription(subscription_data: schemas.NewSubscription, db: Session = Depends(get_db)):
  query = sa.insert(subscriptions).values(**subscription_data.model_dump())
  db.execute(query)
  db.commit()
