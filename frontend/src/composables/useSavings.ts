import { ref } from "vue";
import type { GoalType, SavingAction, NewGoal } from "@/types/savings";
import formatDate from "./formatDate";
import { fetchData } from "./useFetchData";

export default function useSavings() {
  const errorMsg = ref<string>("");
  const loading = ref<boolean>(false);

  const savingsData = ref<GoalType[]>([]);
  const fetchGoals = async () => {
    loading.value = true;

    const { data, error } = await fetchData<GoalType[]>("http://localhost:8000/savings/fetch_all");
    if (error) errorMsg.value = error;
    else savingsData.value = data ?? [];

    loading.value = false;
  }

  const deleteGoal = async(user_id: number, transaction_id: number) => {
    loading.value = true;

    const url = new URL("http://localhost:8000/savings/delete_goal/");
    url.searchParams.append("user_id", user_id.toString());
    url.searchParams.append("goal_id", transaction_id.toString());

    const { error } = await fetchData<GoalType>(url.toString(), {
      method: "DELETE"
    });
    if (error) errorMsg.value = error;

    loading.value = false;
  }

  const totalMonthlySavings = ref<number>(0);
  const fetchTotalMonthlySavings = async (user_id: number, month: string) => {
    loading.value = true;

    const url = new URL("http://localhost:8000/savings/this_month_sum/");
    url.searchParams.append("user_id", user_id.toString());
    url.searchParams.append("month", month);
      
    const { data, error } = await fetchData<number>(url.toString());
    if (error) errorMsg.value = error;
    else totalMonthlySavings.value = data ?? 0;

    loading.value = false;
  }

  const actionsData = ref<SavingAction[]>([]);
  const fetchGoalActions = async(goal_id: number, user_id: number) => {
    loading.value = true;

    const url = new URL("http://localhost:8000/savings/fetch_actions/");
    url.searchParams.append("user_id", user_id.toString());
    url.searchParams.append("goal_id", goal_id.toString());
    
    const { data, error } = await fetchData<SavingAction[]>(url.toString());
    if (error) errorMsg.value = error;
    else actionsData.value = data ?? [];

    loading.value = false;
  }

  const depositFunds = async(amount: number, type: string, goal: GoalType) => {
    loading.value = true;

    const url = new URL(`http://localhost:8000/savings/${type}/`);
    url.searchParams.append("user_id", goal.user_id.toString());
    url.searchParams.append("goal_id", goal.id.toString());
    url.searchParams.append("amount", amount.toString());
    
    const { error } = await fetchData<SavingAction[]>(url.toString(), {
      method: "PUT"
    });
    if (error) errorMsg.value = error;
    else return "success"

    loading.value = false;
  }

  const postNewGoal = async(newGoalData: NewGoal) => {
    loading.value = true;

    const { error } = await fetchData<NewGoal>("http://localhost:8000/savings/new_goal/", {
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

    if (error) errorMsg.value = error;

    loading.value = false;
  }

  const postNewGoalAction = async(action: string, amount: number, goal: GoalType) => {
    loading.value = true;

    const { error } = await fetchData<SavingAction>("http://localhost:8000/savings/new_goal_action/", {
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

    if (error) errorMsg.value = error;
    else return "success";

    loading.value = false;
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