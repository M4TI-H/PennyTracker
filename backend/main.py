from fastapi import FastAPI, Depends, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker, Session
from typing import List
import schemas
from models import users, transactions, expense_category, subscriptions, savings, savings_action

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
  ).limit(4)
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

#delete single transaction
@app.delete("/transactions/delete_one/")
def delete_transaction(db: Session = Depends(get_db), user_id: int = Query(), transaction_id: int = Query()):
  query = sa.delete(
    transactions
  ).where(
    transactions.c.id == transaction_id,
    transactions.c.user_id == user_id
  )

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


# ----- SAVINGS -----

#fetch all savings
@app.get("/savings/fetch_all/", response_model=List[schemas.Savings])
def get_all_savings(db: Session = Depends(get_db)):
  query = sa.select(
    savings
  ).order_by(
    savings.c.creation_date.desc()
  )

  result = db.execute(query)
  rows = result.all()
  return [dict(row._mapping) for row in rows]

#insert new goal
@app.post("/savings/new_goal/")
def post_new_goal(goal_data: schemas.NewSavings, db: Session = Depends(get_db)):

  title = goal_data.title
  amount = goal_data.goal_amount

  if title == "" or title.isspace():
    raise HTTPException(status_code=400, detail="Title cannot be empty.")
  
  if amount <= 0:
    raise HTTPException(status_code=400, detail="Please input correct amount.")

  query = sa.insert(savings).values(**goal_data.model_dump())
  db.execute(query)
  db.commit()

#insert new action (contribution / withdrawal)
@app.post("/savings/new_goal_action")
def post_new_goal_action(action_data: schemas.NewGoalAction, db: Session = Depends(get_db)):
  if action_data.type not in ("deposit", "withdraw"):
    raise HTTPException(status_code=400, detail="Invalid action type.")
  
  #get current amount
  curr_am_query = sa.select(
    savings.c.current_amount,
    savings.c.goal_amount
  ).where(
    savings.c.user_id == action_data.user_id,
    savings.c.id == action_data.goal_id
  )

  row = db.execute(curr_am_query).first()

  if row is None:
    raise HTTPException(status_code=404, detail="Goal does not exist.")

  current_amount = row.current_amount
  goal_amount = row.goal_amount

  if action_data.amount <= 0:
    raise HTTPException(status_code=400, detail="Amount must be positive")
  
  if action_data.type == "withdraw" and action_data.amount > current_amount:
    raise HTTPException(status_code=400, detail="Withdraw amount exceeds current amount")

  new_amount = current_amount + action_data.amount

  if action_data.type == "deposit" and new_amount > goal_amount:
    raise HTTPException(status_code=400, detail="Deposit amount exceeds goal amount")
      
  query = sa.insert(savings_action).values(**action_data.model_dump())
  db.execute(query)
  db.commit()
  return {"status": "success"}

#fetch recent savings actions
@app.get("/savings/fetch_actions/", response_model=List[schemas.GoalAction])
def get_savings_actions(db: Session = Depends(get_db), user_id: int = Query(), goal_id: int = Query()):
  query = sa.select(
    savings_action
  ).where(
    savings_action.c.user_id == user_id,
    savings_action.c.goal_id == goal_id,
  ).order_by(
    savings_action.c.date.desc()
  ).limit(5)

  result = db.execute(query)
  rows = result.all()
  return [dict(row._mapping) for row in rows]

#deposit funds
@app.put("/savings/deposit/")
def deposit_funds(db: Session = Depends(get_db), user_id: int = Query(), goal_id: int = Query(), amount: float = Query()):
  
  #get current amount
  curr_am_query = sa.select(
    savings.c.current_amount,
    savings.c.goal_amount
  ).where(
    savings.c.user_id == user_id,
    savings.c.id == goal_id
  )

  row = db.execute(curr_am_query).first()

  if row is None:
    raise HTTPException(status_code=404, detail="Goal does not exist.")

  current_amount = row.current_amount
  goal_amount = row.goal_amount

  if amount <= 0:
    raise HTTPException(status_code=400, detail="Deposit amount must be positive")
  
  new_amount = current_amount + amount

  if new_amount > goal_amount:
      raise HTTPException(status_code=400, detail="Deposit amount exceeds goal amount")
  finished = 0

  if new_amount == goal_amount:
    finished = 1

  query = sa.update(
    savings
  ).where(
    savings.c.user_id == user_id,
    savings.c.id == goal_id
  ).values(
    current_amount = new_amount,
    finished = finished
  )

  db.execute(query)
  db.commit()

  return {"status": "success"}

#withdraw funds
@app.put("/savings/withdraw/")
def withdraw_funds(db: Session = Depends(get_db), user_id: int = Query(), goal_id: int = Query(), amount: float = Query()):
  
  #get current amount
  curr_am_query = sa.select(
    savings.c.current_amount
  ).where(
    savings.c.user_id == user_id,
    savings.c.id == goal_id
  )
  
  current_amount = db.execute(curr_am_query).scalar_one_or_none()

  if current_amount is None:
    raise HTTPException(status_code=404, detail="Goal does not exist.")

  if amount > current_amount:
    raise HTTPException(status_code=400, detail="Cannot withdraw more than currently deposited.")

  new_amount = current_amount - amount

  query = sa.update(
    savings
  ).where(
    savings.c.user_id == user_id,
    savings.c.id == goal_id
  ).values(
    current_amount = new_amount,
    finished = 0
  )

  db.execute(query)
  db.commit()

  return {"status": "success"}