export interface Budget {
  id: number,
  amount: number,
  month: string,
  user_id: number
}

export interface BudgetShare {
  id: number,
  budget_id: number,
  category_id: number,
  amount: number
}