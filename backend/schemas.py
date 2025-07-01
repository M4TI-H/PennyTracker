from pydantic import BaseModel
from datetime import date

class User(BaseModel):
  id: int
  email: str
  name: str
  class Config:
    from_attributes = True

class Transaction(BaseModel):
  id: int
  name: str
  amount: float
  method: str
  category_name: str
  date: str
  user_id: int
  class Config:
    from_attributes = True

class NewTransaction(BaseModel):
  name: str
  amount: float
  method: str
  category: int
  date: date
  user_id: int

class ExpenseCategory(BaseModel):
  id: int
  name: str
  user_id: int
  class Config:
    from_attributes = True

class Subscription(BaseModel):
  id: int
  service: str
  amount: float
  frequency: str
  start_date: str
  user_id: int
  class Config:
    from_attributes = True

class NewSubscription(BaseModel):
  service: str
  amount: float
  frequency: str
  start_date: date
  user_id: int

class Savings(BaseModel):
  id: int
  title: str
  goal_amount: float
  current_amount: float
  cover: str
  finished: int
  creation_date: str
  user_id: int
  class Config:
    from_attributes = True

class NewSavings(BaseModel):
  title: str
  goal_amount: float
  current_amount: float
  cover: str
  finished: int
  creation_date: date
  user_id: int