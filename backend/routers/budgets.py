from fastapi import Depends, Query, Body, APIRouter
import sqlalchemy as sa
from sqlalchemy.orm import Session
from typing import List
import schemas
from models import budgets, budget_shares, expense_category, transactions
from db import get_db
from datetime import datetime

router = APIRouter(prefix="/budgets", tags=["budgets"])

@router.get("/fetch_budget/")
def fetch_budget(db: Session = Depends(get_db), user_id: int = Query(), month: str = Query()):
  query = sa.select(
    budgets
  ).where(
    budgets.c.user_id == user_id,
    budgets.c.month == month
  )

  result = db.execute(query)
  row = result.first()
  if row is None:
    return {}
  return dict(row._mapping)

@router.put("/update_budget/")
def update_budget(db: Session = Depends(get_db), user_id: int = Query(), month: str = Query(), amount: int = Query()):
  query = sa.update(
    budgets
  ).where(
    budgets.c.user_id == user_id,
    budgets.c.month == month
  ).values(
    amount = amount,
  )

  db.execute(query)
  db.commit()

@router.get("/fetch_shares/")
def fetch_shares(db: Session = Depends(get_db), budget_id: int = Query()):
  query = sa.select(
    budget_shares
  ).where(
    budget_shares.c.budget_id == budget_id,
  )

  rows = db.execute(query).all()
  return [dict(row._mapping) for row in rows]

@router.put("/update_shares/")
def update_shares(db: Session = Depends(get_db), newShares: List[dict] = Body(...)):

  for share in newShares:
    share_id = share["share_id"]
    amount = share["amount"]

    query = sa.update(
      budget_shares
    ).where(
      budget_shares.c.id == share_id
    ).values(
      amount = amount
    )
    db.execute(query)
    
  db.commit()

@router.get("/fetch_summary/")
def fetch_summary(db: Session = Depends(get_db), budget_id: int = Query()):

  query = sa.select(
    expense_category.c.name,
    budget_shares.c.amount.label("total_budget"),
    sa.func.coalesce(sa.func.sum(transactions.c.amount), 0).label("amount_spent")
  ).join(
    budget_shares,
    budget_shares.c.category_id == expense_category.c.id
  ).join(
    budgets,
    budgets.c.id == budget_shares.c.budget_id
  ).outerjoin(
    transactions,
    transactions.c.category == expense_category.c.id
  ).where(
    budgets.c.id == budget_id
  ).group_by(
    expense_category.c.name
  )

  rows = db.execute(query).all()
  return [dict(row._mapping) for row in rows]
