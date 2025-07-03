from fastapi import Depends, Query, HTTPException, APIRouter
import sqlalchemy as sa
from sqlalchemy.orm import Session
from typing import List
import schemas
from models import users
from db import get_db

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/users/", response_model=List[schemas.User])
def get_all_users(db: Session = Depends(get_db)):
  query = sa.select(users)
  result = db.execute(query)
  rows = result.all()
  return [dict(row._mapping) for row in rows]