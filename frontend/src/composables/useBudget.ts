import type { Budget, BudgetShare, BudgetSummary } from "@/types/budgets";
import { ref } from "vue";

export default function useBudget() {
  const budgetData = ref<Budget>();
  const errorMsg = ref<string>("");
  const loading = ref<boolean>(false);

  async function fetchData<FetchType>(url: string, options?: any): Promise<FetchType> {
    try {
      const response = await fetch(url, options);

      if (!response.ok) {
        throw new Error (`HTTP error! Status: ${response.status}`);
      }

      return (await response.json()) as FetchType;
    }
    catch (error: any) {
      errorMsg.value = error.message;
      throw error;
    }
  }
  
  const fetchBudget = async (user_id: number, month_id: string) => {
    loading.value = true;

    const url = new URL("http://localhost:8000/budgets/fetch_budget/");
    url.searchParams.append("user_id", user_id.toString());
    url.searchParams.append("month", month_id);
    
    budgetData.value = await fetchData<Budget>(url.toString());

    loading.value = false;
  }

  const updateBudget = async (amount: number, user_id: number, month_id: string) => {
    loading.value = true;

    const url = new URL("http://localhost:8000/budgets/update_budget");
    url.searchParams.append("amount", amount.toString());
    url.searchParams.append("user_id", user_id.toString());
    url.searchParams.append("month", month_id);

    await fetchData<Budget>(url.toString(), {
      method: "PUT"
    });

    loading.value = false;
  }

  const budgetShares = ref<BudgetShare[]>([]);
  const fetchBudgetShares = async (budget_id: number) => {
    loading.value = true;
    const url = new URL("http://localhost:8000/budgets/fetch_shares/");
    url.searchParams.append("budget_id", budget_id.toString());

    budgetShares.value = await fetchData(url.toString());

    loading.value = false;
  }

  const updateBudgetShares = async (newShares: {share_id: number, amount: number}[]) => {
    loading.value = true;

    await fetchData("http://localhost:8000/budgets/update_shares/", {
      method: "PUT",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(newShares)
    });

    loading.value = false;
  }

  const budgetSummaryData = ref<BudgetSummary[]>([]);
  const fetchBudgetSummary = async (budget_id: number) => {
    loading.value = true;

    const url = new URL("http://localhost:8000/budgets/fetch_summary/");
    url.searchParams.append("budget_id", budget_id.toString());

    budgetSummaryData.value = await fetchData(url.toString());

    loading.value = false;
  }

  return {
    budgetData,
    budgetShares,
    budgetSummaryData,
    errorMsg,
    loading,
    fetchBudget,
    updateBudget,
    fetchBudgetShares,
    updateBudgetShares,
    fetchBudgetSummary
  }
}