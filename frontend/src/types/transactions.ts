export interface Transaction {
  id: number;
  name: string;
  amount: number;
  method: number;
  date: string;
  user_id: number;
  category_name: string;
  method_name: string;
}

export interface NewTransaction {
  name: string | undefined;
  amount: number | undefined;
  method: number | undefined;
  category: number | undefined,
}

export interface Expense {
  category: string;
  method: Record<string, number>;
  total: number;
}

export interface Subscription {
  id: number;
  service: string;
  amount: number;
  frequency: string;
  start_date: string;
  user_id: number;
}

export interface NewSubscription {
  service: string | undefined;
  amount: number | undefined;
  frequency: string | undefined;
  start_date: string | undefined;
}