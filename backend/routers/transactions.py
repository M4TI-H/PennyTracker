from fastapi import Depends, Query, HTTPException, APIRouter
import sqlalchemy as sa
from sqlalchemy.orm import Session
from typing import List
import schemas
from models import transactions, expense_category, subscriptions
from db import get_db

router = APIRouter(prefix="/transactions", tags=["transactions"])

#fetch expense categories
@router.get("/expense_categories/", response_model=List[schemas.ExpenseCategory])
def get_expense_categories(db: Session = Depends(get_db)):
  query = sa.select(expense_category)
  result = db.execute(query)
  rows = result.all()
  return [dict(row._mapping) for row in rows]

#fetch recent transactions, ordered by date
@router.get("/fetch_recent/", response_model=List[schemas.Transaction])
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
@router.get("/fetch_all/", response_model=List[schemas.Transaction])
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
@router.post("/new_expenditure/")
def post_new_expenditure(transaction_data: schemas.NewTransaction, db: Session = Depends(get_db)):

  name = transaction_data.name
  amount = transaction_data.amount
  method = transaction_data.method
  category = transaction_data.category

  if not name or name == "" or name.isspace():
    raise HTTPException(status_code=400, detail="Title cannot be empty.")

  if amount is None or amount <= 0:
    raise HTTPException(status_code=400, detail="Please input correct amount.")
  
  if not method or method.isspace():
    raise HTTPException(status_code=400, detail="Please select the payment method.")

  if category == -1:
    raise HTTPException(status_code=400, detail="Please select the expense category.")

  query = sa.insert(transactions).values(**transaction_data.model_dump())
  db.execute(query)
  db.commit()

#delete single transaction
@router.delete("/delete_one/")
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
@router.get("/fetch_by_category")
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
@router.get("/fetch_by_method")
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