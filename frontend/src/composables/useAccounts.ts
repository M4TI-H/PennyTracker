import { ref } from "vue";
import type { Account } from "@/types/options";
import { fetchData } from "./useFetchData";

export default function useAccounts () {
  const accountsData = ref<Account[]>([]);
  const errorMsg = ref<string>("");
  const loading = ref<boolean>(false);

  const fetchAccounts = async (user: number) => {
    loading.value = true;

    const url = new URL("http://localhost:8000/transactions/fetch_accounts");
    url.searchParams.append("user_id", user.toString());
    
    const { data, error } = await fetchData<Account[]>(url.toString());
    if (error) errorMsg.value = error;
    else accountsData.value = data ?? [];

    loading.value = false;
  }

  const fetchTopAccounts = async(user: number) => {
    loading.value = true;

    const url = new URL("http://localhost:8000/transactions/fetch_top_accounts");
    url.searchParams.append("user_id", user.toString());
    
    const { data, error } = await fetchData<Account[]>(url.toString());
    if (error) errorMsg.value = error;
    else accountsData.value = data ?? [];

    loading.value = false;
  }

  const postNewAccount = async (user_id: number, name: string) => {
    loading.value = true;

    const { error } = await fetchData<Account[]>("http://localhost:8000/transactions/new_account/", {
      method: "POST",
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        name: name,
        isActive: 1,
        user_id: user_id
      })
    });

    if (error) errorMsg.value = error;

    loading.value = false;
  }

  const deleteAccount = async (account_id: number, user_id: number) => {
    loading.value = true;

    const url = new URL("http://localhost:8000/transactions/delete_account/");
    url.searchParams.append("account_id", account_id.toString());
    url.searchParams.append("user_id", user_id.toString());

    const { error } = await fetchData<Account[]>(url.toString(), {
      method: "DELETE"
    });

    if (error) errorMsg.value = error;
    
    loading.value = false;
  }

  const changeActivity = async (account_id: number, user_id: number, activity: number) => {
    loading.value = true;

    const url = new URL("http://localhost:8000/transactions/change_account_activity/");
    url.searchParams.append("account_id", account_id.toString());
    url.searchParams.append("user_id", user_id.toString());
    url.searchParams.append("activity", activity.toString());

    const { error } = await fetchData<Account[]>(url.toString(), {
      method: "PUT"
    });

    if (error) errorMsg.value = error;
    
    loading.value = false;
  }

  const fetchActiveAccounts = async (user: number) => {
    loading.value = true;

    const url = new URL("http://localhost:8000/transactions/fetch_active_accounts");
    url.searchParams.append("user_id", user.toString());
    
    const { data, error } = await fetchData<Account[]>(url.toString());
    if (error) errorMsg.value = error;
    else accountsData.value = data ?? [];

    loading.value = false;
  }

  return {
    accountsData,
    errorMsg,
    loading,
    fetchAccounts,
    fetchTopAccounts,
    postNewAccount,
    deleteAccount,
    changeActivity,
    fetchActiveAccounts
  }
}
