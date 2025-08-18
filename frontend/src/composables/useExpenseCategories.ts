import { ref } from "vue";
import type { Category } from "@/types/options";
import { fetchData } from "./useFetchData";

export default function useExpenseCategories() {
  const errorMsg = ref<string>("");
  const loading = ref<boolean>(false);

  const expenseCategories = ref<Category[]>([]);
  const fetchExpenseCategories = async(user: number) => {
    loading.value = true;

    const url = new URL("http://localhost:8000/transactions/expense_categories");
    url.searchParams.append("user_id", user.toString());

    const { data, error } = await fetchData<Category[]>(url.toString());
    if (error) errorMsg.value = error;
    else expenseCategories.value = data ?? [];

    loading.value = false;
  }

  const postNewCategory = async (user_id: number, newCategory: string) => {
    loading.value = true;

    const { error } = await fetchData<Category>("http://localhost:8000/transactions/new_category/", {
      method: "POST",
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        name: newCategory,
        isActive: 1,
        user_id: user_id
      })
    });

    if (error) errorMsg.value = error;
    
    loading.value = false;
  }

  const deleteCategory = async (user_id: number, category_id: number) => {
    loading.value = true;

    const url = new URL("http://localhost:8000/transactions/delete_category/");
    url.searchParams.append("category_id", category_id.toString());
    url.searchParams.append("user_id", user_id.toString());

    const { error } = await fetchData<Category>(url.toString(), {
      method: "DELETE"
    });

    if (error) errorMsg.value = error;
    
    loading.value = false;
  }

  const fetchActiveCategories = async (user: number) => {
    loading.value = true;

    const url = new URL("http://localhost:8000/transactions/fetch_active_categories");
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
    fetchExpenseCategories,
    postNewCategory,
    deleteCategory,
    fetchActiveCategories
  }
}