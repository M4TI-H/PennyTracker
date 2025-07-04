from fastapi import Depends, Query, HTTPException, APIRouter
import sqlalchemy as sa
from sqlalchemy.orm import Session
from typing import List
import schemas
from models import savings, savings_action
from db import get_db

router = APIRouter(prefix="/savings", tags=["savings"])

#fetch all savings
@router.get("/fetch_all/", response_model=List[schemas.Savings])
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
@router.post("/new_goal/")
def post_new_goal(goal_data: schemas.NewSavings, db: Session = Depends(get_db)):

  title = goal_data.title
  amount = goal_data.goal_amount

  if title == "" or title.isspace():
    raise HTTPException(status_code=400, detail="Title cannot be empty.")
  
  if amount is None or amount <= 0:
    raise HTTPException(status_code=400, detail="Please input correct amount.")

  query = sa.insert(savings).values(**goal_data.model_dump())
  db.execute(query)
  db.commit()

#insert new action (contribution / withdrawal)
@router.post("/new_goal_action")
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
@router.get("/fetch_actions/", response_model=List[schemas.GoalAction])
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
@router.put("/deposit/")
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
@router.put("/withdraw/")
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

#delete goal
@router.delete("/delete_goal/")
def delete_goal(db: Session = Depends(get_db), user_id: int = Query(), goal_id: int = Query()):

  query1 = sa.delete(
    savings_action
  ).where(
    savings_action.c.goal_id == goal_id,
    savings_action.c.user_id == user_id,
    
  )

  db.execute(query1)
  db.commit()

  query2 = sa.delete(
    savings
  ).where(
    savings.c.id == goal_id,
    savings.c.user_id == user_id
  )

  db.execute(query2)
  db.commit()

#total savings this month
@router.get("/this_month_sum/")
def monthly_sum(db: Session = Depends(get_db), user_id: int = Query(), month: str = Query()):
  
  date_pattern = f"%/{month}/%"

  query_deposits = sa.select(
    sa.func.sum(savings_action.c.amount)
  ).where(
    savings_action.c.type == "deposit",
    savings_action.c.date.like(date_pattern),
    savings_action.c.user_id == user_id,
  )

  deposit_sum = db.execute(query_deposits).scalar_one_or_none()

  query_withdrawals = sa.select(
    sa.func.sum(savings_action.c.amount)
  ).where(
    savings_action.c.type == "withdraw",
    savings_action.c.date.like(date_pattern),
    savings_action.c.user_id == user_id,
  )

  withdrawal_sum = db.execute(query_withdrawals).scalar_one_or_none()

  if deposit_sum and withdrawal_sum:
      return deposit_sum - withdrawal_sum
  elif deposit_sum and not withdrawal_sum:
    return deposit_sum
  elif not deposit_sum and withdrawal_sum:
    return -1 * withdrawal_sum
  else:
    return 0