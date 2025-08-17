from fastapi import Depends, Query, HTTPException, APIRouter
import sqlalchemy as sa
from sqlalchemy.orm import Session
from typing import List
import schemas
from models import transactions, expense_category, accounts
from db import get_db

router = APIRouter(prefix="/transactions", tags=["transactions"])

#fetch expense categories
@router.get("/expense_categories/")
def get_expense_categories(db: Session = Depends(get_db), user_id: int = Query()):
  query = sa.select(
    expense_category
  ).where(
    expense_category.c.user_id == user_id
  )
  result = db.execute(query)
  rows = result.all()
  return [dict(row._mapping) for row in rows]

#fetch recent transactions, ordered by date
@router.get("/fetch_recent/")
def get_recent_transactions(db: Session = Depends(get_db)):
  query = sa.select(
    transactions,
    expense_category.c.name.label("category_name"),
    accounts.c.name.label("method_name")
  ).join(
    expense_category,
    transactions.c.category == expense_category.c.id
  ).join(
    accounts,
    transactions.c.method == accounts.c.id,
  ).order_by(
    transactions.c.date.desc()
  ).limit(4)

  result = db.execute(query)
  rows = result.all()
  return [dict(row._mapping) for row in rows]

#fetch all transactions
@router.get("/fetch_all/")
def get_all_transactions(db: Session = Depends(get_db)):
  query = sa.select(
    transactions,
    expense_category.c.name.label("category_name"),
    accounts.c.name.label("method_name")
  ).join(
    expense_category,
    transactions.c.category == expense_category.c.id
  ).join(
    accounts,
    transactions.c.method == accounts.c.id,
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
  
  if method == -1:
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
  date_pattern = f"%/{month}/%"

  query = sa.select(
    expense_category.c.name,
    accounts.c.name.label("method_name"),
    sa.func.sum(transactions.c.amount),
  ).join(
    transactions,
    transactions.c.category == expense_category.c.id
  ).join(
    accounts,
    transactions.c.method == accounts.c.id,
  ).where(
    transactions.c.user_id == user_id,
    transactions.c.date.like(date_pattern)
  ).group_by(
    expense_category.c.name,
    accounts.c.name
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
  date_pattern = f"%/{month}/%"

  query = sa.select(
    expense_category.c.name,
    accounts.c.name.label("method_name"),
    sa.func.sum(transactions.c.amount)
  ).join(
    transactions,
    transactions.c.category == expense_category.c.id
  ).join(
    accounts,
    transactions.c.method == accounts.c.id,
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

#add new category
@router.post("/new_category/")
def post_new_category(category_data: schemas.NewExpenseCategory, db: Session = Depends(get_db)):
  name = category_data.name

  if not name or name.isspace() or name == "":
    raise HTTPException(status_code=400, detail="Please select correct category name.")

  query = sa.insert(expense_category).values(**category_data.model_dump())
  db.execute(query)
  db.commit()

#delete category and clear all transactions of this type
@router.delete("/delete_category/")
def delete_category(db: Session = Depends(get_db), user_id: int = Query(), category_id: int = Query()):
  query1 = sa.delete(
    transactions
  ).where(
    transactions.c.category == category_id,
    transactions.c.user_id == user_id
  )

  db.execute(query1)
  db.commit()

  query2 = sa.delete(
    expense_category
  ).where(
    expense_category.c.id == category_id,
    expense_category.c.user_id == user_id
  )
    
  db.execute(query2)
  db.commit()

#fetch all accounts
@router.get("/fetch_accounts/", response_model=List[schemas.Account])
def fetch_accounts(db: Session = Depends(get_db), user_id: int = Query()):
  query = sa.select(
    accounts,
    sa.func.coalesce(sa.func.sum(transactions.c.amount), 0).label("expenses"),
  ).outerjoin(
    transactions,
    transactions.c.method == accounts.c.id
  ).where(
    accounts.c.user_id == user_id,
  ).group_by(
    accounts.c.id,
  )

  rows = db.execute(query).all()
  return [dict(row._mapping) for row in rows]


#fetch top accounts
@router.get("/fetch_top_accounts/", response_model=List[schemas.Account])
def fetch_top_accounts(db: Session = Depends(get_db), user_id: int = Query()):
  query = sa.select(
    accounts,
    sa.func.coalesce(sa.func.sum(transactions.c.amount), 0).label("expenses"),
  ).outerjoin(
    transactions,
    transactions.c.method == accounts.c.id
  ).where(
    accounts.c.user_id == user_id,
  ).group_by(
    accounts.c.id
  ).order_by(
    sa.func.coalesce(sa.func.sum(transactions.c.amount), 0).desc()
  ).limit(3)

  rows = db.execute(query).all()
  return [dict(row._mapping) for row in rows]


#create new account 
@router.post("/new_account/")
def add_new_account(account_data: schemas.NewAccount, db: Session = Depends(get_db)):
  name = account_data.name

  if not name or name.isspace() or name == "":
    raise HTTPException(status_code=400, detail="Please select correct account name.")
  
  query = sa.insert(accounts).values(**account_data.model_dump())
  db.execute(query)
  db.commit()

#delete account with all its transactions
@router.delete("/delete_account/")
def delete_account(db: Session = Depends(get_db), user_id: int = Query(), account_id: int = Query()):
  query1 = sa.delete(
    transactions
  ).where(
    transactions.c.method == account_id,
    transactions.c.user_id == user_id
  )

  db.execute(query1)
  db.commit()

  query2 = sa.delete(
    accounts
  ).where(
    accounts.c.id == account_id,
    accounts.c.user_id == user_id
  )
    
  db.execute(query2)
  db.commit()

#fetch all transactions and group by month
@router.get("/monthly_transactions/", response_model=List[schemas.MonthlyTransactions])
def get_monthly_transactions(db: Session = Depends(get_db), user_id: int = Query()):
  date_parsed = sa.func.str_to_date(transactions.c.date, '%d/%m/%Y')

  query = sa.select(
    sa.func.date_format(date_parsed, '%Y-%m').label("month"),
    sa.func.sum(transactions.c.amount).label("total_expenses"),
    sa.func.count().label("number_of_transactions")
  ).group_by(
    sa.func.date_format(date_parsed, '%Y-%m')
  ).where(
    transactions.c.user_id == user_id
  ).order_by(
    sa.func.date_format(date_parsed, '%Y-%m').asc()
  ).limit(12)
  
  result = db.execute(query)
  rows = result.all()
  return [dict(row._mapping) for row in rows]

#count transactions by date
@router.get("/transactions_count/", response_model=List[schemas.TransactionsCount])
def get_transactions_count(db: Session = Depends(get_db), user_id: int = Query()):
  query = sa.select(
    transactions.c.id,
    transactions.c.date,
    sa.func.count(transactions.c.id).label("number_of_transactions")
  ).group_by(
     transactions.c.date
  ).where(
    transactions.c.user_id == user_id
  ).order_by(
    transactions.c.date.desc()
  )

  result = db.execute(query)
  rows = result.all()
  return [dict(row._mapping) for row in rows]

@router.get("/transactions_months/")
def get_transactions_months(db: Session = Depends(get_db), user_id: int = Query()):
  query = sa.select(
    transactions.c.date
  ).where(
    transactions.c.user_id == user_id
  )

  result = db.execute(query).scalars().all()

  months = set()
  for d in result:
    day, month, year = d.split("/")
    months.add(f"{month}/{year}")
  
  return sorted(list(months), reverse=True)