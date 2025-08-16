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

export interface BudgetSummary {
  name: string,
  total_budget: number,
  amount_spent: number
}