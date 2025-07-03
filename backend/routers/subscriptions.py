from fastapi import Depends, Query, HTTPException, APIRouter
import sqlalchemy as sa
from sqlalchemy.orm import Session
from typing import List
import schemas
from models import subscriptions
from db import get_db

router = APIRouter(prefix="/subscriptions", tags=["subscriptions"])

#fetch all subscriptions
@router.get("/fetch_all/", response_model=List[schemas.Subscription])
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
@router.post("/new_subscription/")
def post_new_subscription(subscription_data: schemas.NewSubscription, db: Session = Depends(get_db)):
  query = sa.insert(subscriptions).values(**subscription_data.model_dump())
  db.execute(query)
  db.commit()
