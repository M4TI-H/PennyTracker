import { ref } from "vue";
import type { MonthlyTransactions } from "@/types/transactions";

export default function useMonthlyTransactions() {
  const monthlyTransactionsData = ref<MonthlyTransactions[]>([]);
  const errorMsg = ref<string>("");
  const loading = ref<boolean>(false);

  const fetchMonthlyTransactions = async (user_id: number) => {
    loading.value = true;

   try {
    const url = new URL("http://localhost:8000/transactions/monthly_transactions/");
    url.searchParams.append("user_id", user_id.toString());
    
    const response = await fetch(url.toString());

    if (!response.ok) {
      throw new Error (`HTTP error! Status: ${response.status}`);
    }

    monthlyTransactionsData.value = await response.json();
  }
  catch (error: any) {
    errorMsg.value = error.message;
    console.error(`An error has occured while fetching transactions data: ${error}`);
  }

  loading.value = false;
  }


  return {
    monthlyTransactionsData,
    errorMsg,
    loading,
    fetchMonthlyTransactions
  }
}