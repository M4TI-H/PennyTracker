from fastapi import Depends, Query, HTTPException, APIRouter
import sqlalchemy as sa
from sqlalchemy.orm import Session
from typing import List
import schemas
from models import budgets
from db import get_db

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