import type { Budget, BudgetShare, BudgetSummary } from "@/types/budgets";
import { ref } from "vue";
import { fetchData } from "./useFetchData";

export default function useBudget() {
  const budgetData = ref<Budget>();
  const errorMsg = ref<string>("");
  const loading = ref<boolean>(false);
  
  const fetchBudget = async (user_id: number, month_id: string) => {
    loading.value = true;

    const url = new URL("http://localhost:8000/budgets/fetch_budget/");
    url.searchParams.append("user_id", user_id.toString());
    url.searchParams.append("month", month_id);
    
    const { data, error } = await fetchData<Budget>(url.toString());
    if (error) errorMsg.value = error;
    else budgetData.value = data;

    loading.value = false;
  }

  const updateBudget = async (amount: number, user_id: number, month_id: string) => {
    loading.value = true;

    const url = new URL("http://localhost:8000/budgets/update_budget");
    url.searchParams.append("amount", amount.toString());
    url.searchParams.append("user_id", user_id.toString());
    url.searchParams.append("month", month_id);

    const { error } = await fetchData<Budget>(url.toString(), {
      method: "PUT"
    });

    if (error) errorMsg.value = error;

    loading.value = false;
  }

  const budgetShares = ref<BudgetShare[]>([]);
  const fetchBudgetShares = async (budget_id: number) => {
    loading.value = true;
    const url = new URL("http://localhost:8000/budgets/fetch_shares/");
    url.searchParams.append("budget_id", budget_id.toString());

    const { data, error } = await fetchData<BudgetShare[]>(url.toString());
    if (error) errorMsg.value = error;
    else budgetShares.value = data ?? [];

    loading.value = false;
  }

  const updateBudgetShares = async (newShares: {share_id: number, amount: number}[]) => {
    loading.value = true;

    const { error } = await fetchData("http://localhost:8000/budgets/update_shares/", {
      method: "PUT",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(newShares)
    });

    if (error) errorMsg.value = error;

    loading.value = false;
  }

  const budgetSummaryData = ref<BudgetSummary[]>([]);
  const fetchBudgetSummary = async (budget_id: number) => {
    loading.value = true;

    const url = new URL("http://localhost:8000/budgets/fetch_summary/");
    url.searchParams.append("budget_id", budget_id.toString());

    const { data, error } = await fetchData<BudgetSummary[]>(url.toString());
    
    if (error) errorMsg.value = error;
    else budgetSummaryData.value = data ?? [];

    loading.value = false;
  }

  const currentBudgetExists = ref<boolean>(false);
  const checkExistenceOfBudget = async (user_id: number, month_id: string) => {
    loading.value = true;

    const url = new URL("http://localhost:8000/budgets/check_existence/");
    url.searchParams.append("user_id", user_id.toString());
    url.searchParams.append("month_id", month_id.toString());

    const { data, error } = await fetchData<boolean>(url.toString());
    
    if (error) errorMsg.value = error;
    else currentBudgetExists.value = data ?? false;

    loading.value = false;
  }

  const createNewBudget = async(user_id: number, month_id: string) => {
    loading.value = true;

    const { data, error } = await fetchData("http://localhost:8000/budgets/create_budget/", {
      method: "POST",
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        user_id: user_id,
        month: month_id,
        amount: 1000
      })
    });
    
    if (error) errorMsg.value = error;

    loading.value = false;
  }

  const budgetMonths = ref<string[]>([]);
  //fetch names of months with transactions
  const fetchBudgetMonths = async (user_id: number) => {
    loading.value = true;

    const url = new URL("http://localhost:8000/budgets/budget_months/");
    url.searchParams.append("user_id", user_id.toString());

    const { data, error} = await fetchData<string[]>(url.toString());
    if (error) errorMsg.value = error;
    else budgetMonths.value = data ?? [];

    loading.value = false;
  }

  return {
    budgetData,
    budgetShares,
    budgetSummaryData,
    currentBudgetExists,
    budgetMonths,
    errorMsg,
    loading,
    fetchBudget,
    updateBudget,
    fetchBudgetShares,
    updateBudgetShares,
    fetchBudgetSummary,
    checkExistenceOfBudget,
    createNewBudget,
    fetchBudgetMonths
  }
}