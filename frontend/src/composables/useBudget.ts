import type { Budget } from "@/types/budgets";
import { ref } from "vue";

export default function useBudget() {
  const budgetData = ref<Budget>();
  const budgetShares = ref<any[]>([]);
  const errorMsg = ref<string>("");
  const loading = ref<boolean>(false);
  
  const fetchBudget = async (user_id: number, month_id: string) => {
    try {
      const url = new URL("http://localhost:8000/budgets/fetch_budget/");
      url.searchParams.append("user_id", user_id.toString());
      url.searchParams.append("month", month_id);
      
      const response = await fetch(url.toString());

      if (!response.ok) {
        throw new Error (`HTTP error! Status: ${response.status}`);
      }

      budgetData.value = await response.json();
    }
    catch (error: any) {
      errorMsg.value = error.message;
      console.error(`An error has occured while fetching budget data: ${error}`);
    }
  }

  const updateBudget = async (amount: number, user_id: number, month_id: string) => {
    try {
      const url = new URL("http://localhost:8000/budgets/update_budget");
      url.searchParams.append("amount", amount.toString());
      url.searchParams.append("user_id", user_id.toString());
      url.searchParams.append("month", month_id);
      
      const response = await fetch(url.toString(), {
        method: "PUT"
      });

      if (!response.ok) {
        const err = await response.json()
        throw new Error(err.detail);
      }
    }
    catch (error: any) {
      errorMsg.value = error.message;
      console.error(`An error has occured while updating budget data: ${error}`);
    }
  }

  return {
    budgetData,
    budgetShares,
    errorMsg,
    loading,
    fetchBudget,
    updateBudget
  }
}