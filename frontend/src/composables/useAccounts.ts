import { ref } from "vue";
import type { Account } from "@/types/options";

export default function useAccounts () {
  const accountsData = ref<Account[]>([]);
  const errorMsg = ref<string>("");
  const loading = ref<boolean>(false);

  const fetchAccounts = async (user: number) => {
    loading.value = true;

    try {
      const url = new URL("http://localhost:8000/transactions/fetch_accounts");
      url.searchParams.append("user_id", user.toString());
      
      const response = await fetch(url.toString());

      if (!response.ok) {
        throw new Error (`HTTP error! Status: ${response.status}`);
      }

      accountsData.value = await response.json();
    }
    catch (error: any) {
      errorMsg.value = error.message;
      console.error(`An error has occured while fetching accounts data: ${error}`);
    }

    loading.value = false;
  }

  const fetchTopAccounts = async(user: number) => {
    loading.value = true;

    try {
      const url = new URL("http://localhost:8000/transactions/fetch_top_accounts");
      url.searchParams.append("user_id", user.toString());
      
      const response = await fetch(url.toString());

      if (!response.ok) {
        throw new Error (`HTTP error! Status: ${response.status}`);
      }

      accountsData.value = await response.json();
    }
    catch (error: any) {
      errorMsg.value = error.message;
      console.error(`An error has occured while fetching accounts data: ${error}`);
    }

    loading.value = false;
  }

  const postNewAccount = async (user_id: number, name: string) => {
    loading.value = true;
    try {
      const response = await fetch("http://localhost:8000/transactions/new_account/", {
        method: "POST",
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          name: name,
          user_id: user_id
        })
      });
      
      if (!response.ok) {
        const err = await response.json()
        throw new Error(err.detail); 
      }
    }
    catch (error: any) {
      errorMsg.value = error.message;
      console.error(`An error has occured while posting new account: ${error}`);
    }

    loading.value = false;
  }

  return {
    accountsData,
    errorMsg,
    loading,
    fetchAccounts,
    fetchTopAccounts,
    postNewAccount
  }
}
