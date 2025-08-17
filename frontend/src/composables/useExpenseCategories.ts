import { ref } from "vue";
import type { Category } from "@/types/options";
import { fetchData } from "./useFetchData";

export default function useExpenseCategories() {
  const expenseCategories = ref<Category[]>([]);
  const errorMsg = ref<string>("");
  const loading = ref<boolean>(false);

  const fetchExpenseCategories = async(user: number) => {
    loading.value = true;

    const url = new URL("http://localhost:8000/transactions/expense_categories");
    url.searchParams.append("user_id", user.toString());

    const { data, error } = await fetchData<Category[]>(url.toString());
    if (error) errorMsg.value = error;
    else expenseCategories.value = data ?? [];

    loading.value = false;
  }

  return {
    expenseCategories,
    errorMsg,
    loading,
    fetchExpenseCategories
  }
}