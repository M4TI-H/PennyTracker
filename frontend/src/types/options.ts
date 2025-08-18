export interface Account {
  id: number;
  name: string;
  isActive: number;
  user_id: number;
  expenses: number;
}

export interface Category {
  id: number;
  name: string;
  isActive: number;
  user_id: number;
}