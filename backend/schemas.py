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
  method_name: str
  category_name: str
  date: str
  user_id: int
  class Config:
    from_attributes = True

class NewTransaction(BaseModel):
  name: str
  amount: float
  method: int
  category: int
  date: str
  user_id: int

class MonthlyTransactions(BaseModel):
  month: str
  total_expenses: float
  number_of_transactions: int
  class Config:
    from_attributes = True

class TransactionsCount(BaseModel):
  id: int
  date: str
  number_of_transactions: int
  class Config:
    from_attributes = True

class ExpenseCategory(BaseModel):
  id: int
  name: str
  isActive: int
  user_id: int
  class Config:
    from_attributes = True

class NewExpenseCategory(BaseModel):
  name: str
  isActive: int
  user_id: int

class Account(BaseModel):
  id: int
  name: str
  isActive: int
  user_id: int
  expenses: float
  class Config:
    from_attributes = True

class NewAccount(BaseModel):
  name: str
  isActive: int
  user_id: int
  
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
  start_date: str
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
  creation_date: str
  user_id: int

class UpdateGoalCurrentAmount(BaseModel):
  id: int
  current_amount: float
  user_id: int
  finished: int

class GoalAction(BaseModel):
  id: int
  type: str
  amount: float
  date: str
  goal_id: int
  user_id: int
  class Config:
    from_attributes = True

class NewGoalAction(BaseModel):
  type: str
  amount: float
  date: str
  goal_id: int
  user_id: int

class Budget(BaseModel):
  id: int
  amount: float
  user_id: int
  month: str
  class Config:
    from_attributes = True

class NewBudget(BaseModel):
  amount: float
  month: str
  user_id: int

class Share(BaseModel):
  id: int
  amount: float
  budget_id: int
  category_id: int
  class Config:
    from_attributes = True

class BudgetSummary(BaseModel):
  name: str
  total_budget: float
  amount_spent: float
  class Config:
    from_attributes = True