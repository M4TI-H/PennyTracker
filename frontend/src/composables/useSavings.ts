import { ref } from "vue";
import type { GoalType, SavingAction, NewGoal } from "@/types/savings";
import formatDate from "./formatDate";

export default function useSavings() {
  const savingsData = ref<GoalType[]>([]);
  const totalMonthlySavings = ref<number>(0);
  const actionsData = ref<SavingAction[]>([]);
  const errorMsg = ref<string>("");
  const loading = ref<boolean>(false);

  const fetchGoals = async() => {
    loading.value = true;

    try {
      const response = await fetch("http://localhost:8000/savings/fetch_all");
      if (!response.ok) {
        throw new Error (`HTTP error! Status: ${response.status}`);
      }

      savingsData.value = await response.json();
    }
    catch (error: any) {
      errorMsg.value = error.message;
      console.error(`An error has occured while fetching savings data: ${error}`);
    }

    loading.value = false;
  }

  const deleteGoal = async(user_id: number, transaction_id: number) => {
    loading.value = true;
    try {
      const url = new URL("http://localhost:8000/savings/delete_goal/");
      url.searchParams.append("user_id", user_id.toString());
      url.searchParams.append("goal_id", transaction_id.toString());

      const response = await fetch(url.toString(), {
        method: "DELETE"
      });

      if (!response.ok) {
        throw new Error (`HTTP error! Status: ${response.status}`);
      }

    }
    catch (error: any) {
      errorMsg.value = error.message;
      console.error(`An error has occured while deleting a saving goal: ${error}`);
    }
    loading.value = false;
  }

  const fetchTotalMonthlySavings = async (user_id: number, month: string) => {
    loading.value = true;

    try {
      const url = new URL("http://localhost:8000/savings/this_month_sum/");
      url.searchParams.append("user_id", user_id.toString());
      url.searchParams.append("month", month);
      
      const response = await fetch(url.toString());

      if (!response.ok) {
        throw new Error (`HTTP error! Status: ${response.status}`);
      }

      totalMonthlySavings.value = await response.json();
    }
    catch (error: any) {
      errorMsg.value = error.message;
      console.error(`An error has occured while fetching data: ${error}`);
    }
    loading.value = false;
  }

  const fetchGoalActions = async(goal_id: number, user_id: number) => {
    try {
      const url = new URL("http://localhost:8000/savings/fetch_actions/");
      url.searchParams.append("user_id", user_id.toString());
      url.searchParams.append("goal_id", goal_id.toString());
      
      const response = await fetch(url.toString());

      if (!response.ok) {
        throw new Error (`HTTP error! Status: ${response.status}`);
      }

      actionsData.value = await response.json();
    }
    catch (error) {
      console.error(`An error has occured while fetching savings actions data: ${error}`);
    }
  }

  const depositFunds = async(amount: number, type: string, goal: GoalType) => {
    try {
      const url = new URL(`http://localhost:8000/savings/${type}/`);
      url.searchParams.append("user_id", goal.user_id.toString());
      url.searchParams.append("goal_id", goal.id.toString());
      url.searchParams.append("amount", amount.toString());
      
      const response = await fetch(url.toString(), {
        method: "PUT"
      });

      if (!response.ok) {
        const err = await response.json()
        throw new Error(err.detail);
      }

      const result = await response.json();

      return result.status;
    }
    catch (error) {
      console.error(`An error has occured while fetching savings actions data: ${error}`);
    }
  }

  const postNewGoal = async(newGoalData: NewGoal) => {
    try {
      const response = await fetch("http://localhost:8000/savings/new_goal/", {
        method: "POST",
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          title: newGoalData.title, 
          goal_amount: newGoalData.amount ? newGoalData.amount : -1, 
          current_amount: 0.0,
          cover: newGoalData.cover || "#000000",
          finished: 0,
          creation_date: formatDate(new Date()),
          user_id: newGoalData.user_id
        })
      });

      if (!response.ok) {
        const err = await response.json()
        throw new Error(err.detail);
      }
      
    }
    catch (error: any) {
      console.error(`An error has occured while posting savings data: ${error}`);
    }
  }

  const postNewGoalAction = async(action: string, amount: number, goal: GoalType) => {
    try {
      const response = await fetch("http://localhost:8000/savings/new_goal_action/", {
        method: "POST",
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          type: action, 
          amount: amount, 
          date: formatDate(new Date()),
          goal_id: goal.id,
          user_id: goal.user_id
        })
      });

      if (!response.ok) {
        const err = await response.json()
        throw new Error(err.detail);
      }

      const result = await response.json();

      return result.status;
    }
    catch (error) {
      console.error(`An error has occured while posting savings actions data: ${error}`);
    }
  }

  return {
    savingsData,
    totalMonthlySavings,
    actionsData,
    errorMsg,
    loading,
    fetchTotalMonthlySavings,
    fetchGoals,
    deleteGoal,
    fetchGoalActions,
    depositFunds,
    postNewGoal,
    postNewGoalAction
  }
}