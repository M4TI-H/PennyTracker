export interface SavingAction {
  id: number;
  type: "deposit" | "withdraw";
  amount: number;
  date: string;
  goal_id: number;
  user_id: number;
}

export interface GoalType {
  id: number;
  title: string;
  current_amount: number;
  goal_amount: number;
  creation_date: string;
  finished: number;
  user_id: number;
  cover: string;
}

export interface NewGoal {
  title: string | undefined;
  amount: number | null;
  cover: string;
  user_id: number;
}
