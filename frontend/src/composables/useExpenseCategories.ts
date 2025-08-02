import { ref } from "vue";
import type { Category } from "@/types/options";

export default function useExpenseCategories() {
  const expenseCategories = ref<Category[]>([]);
  const errorMsg = ref<string>("");
  const loading = ref<boolean>(false);

  const fetchExpenseCategories = async(user: number) => {
    loading.value = true;

    try {
      const url = new URL("http://localhost:8000/transactions/expense_categories");
      url.searchParams.append("user_id", user.toString());

      const response = await fetch(url.toString());

      if (!response.ok) {
        throw new Error (`HTTP error! Status: ${response.status}`);
      }

      expenseCategories.value = await response.json();
    }
    catch (error: any) {
      errorMsg.value = error.message;
      console.error(`An error has occured while fetching categories data: ${error}`);
    }
    loading.value = false;
  }

  return {
    expenseCategories,
    errorMsg,
    loading,
    fetchExpenseCategories
  }
}