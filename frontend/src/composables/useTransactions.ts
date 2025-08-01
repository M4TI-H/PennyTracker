import { ref } from "vue";
import type { Transaction, NewTransaction, Expense } from "@/types/transactions";
import formatDate from "./formatDate";

export default function useTransactions() {
  const transactionsData = ref<Transaction[]>([]);
  const expenses = ref<Expense[]>([]);
  const totalExpenses = ref<number>(0);
  const errorMsg = ref<string>("");
  const loading = ref<boolean>(false);

  const fetchTransactions = async() => {
    try {
      const response = await fetch("http://localhost:8000/transactions/fetch_all");
      if (!response.ok) {
        throw new Error (`HTTP error! Status: ${response.status}`);
      }

      transactionsData.value = await response.json();
    }
    catch (error) {
      console.error(`An error has occured while fetching transactions data: ${error}`);
    }
  }

  const deleteTransaction = async(user_id: number, transaction: number) => {
    try {
      const url = new URL("http://localhost:8000/transactions/delete_one");
      url.searchParams.append("user_id", user_id.toString());
      url.searchParams.append("transaction_id", transaction.toString());

      const response = await fetch(url.toString(), {
        method: "DELETE"
      });

      if (!response.ok) {
        throw new Error (`HTTP error! Status: ${response.status}`);
      }

    }
    catch (error) {
      console.error(`An error has occured while deleting a transaction: ${error}`);
    }
  }

  const fetchRecentTransactions = async() => {
    try {
      const response = await fetch("http://localhost:8000/transactions/fetch_recent/");
      if (!response.ok) {
        throw new Error (`HTTP error! Status: ${response.status}`);
      }

      transactionsData.value = await response.json();
    }
    catch (error) {
      console.error(`An error has occured while fetching transactions data: ${error}`);
    }
  }

  const postNewExpenditure = async(newExpData: NewTransaction, user_id: number) => {
    try {
      const response = await fetch("http://localhost:8000/transactions/new_expenditure/", {
        method: "POST",
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          name: newExpData.name, 
          amount: newExpData.amount ? newExpData.amount : 0,
          method: newExpData.method ? newExpData.method : -1, 
          category: newExpData.category ? newExpData.category : -1,
          date: formatDate(new Date()).slice(0, 10),
          user_id: user_id
        })
      });

      if (!response.ok) {
        const err = await response.json()
        throw new Error(err.detail); 
      }

    }
    catch (error) {
      console.error(`An error has occured while posting transactions data: ${error}`);
    }
  }
  
  const fetchExpensesByCategory = async (user_id: number, month: string) => {
    try {
      const url = new URL("http://localhost:8000/transactions/fetch_by_category");
      url.searchParams.append("user_id", user_id.toString());
      url.searchParams.append("month", month);
      
      const response = await fetch(url.toString());

      if (!response.ok) {
        throw new Error (`HTTP error! Status: ${response.status}`);
      }

      const fetchedData = await response.json();
      expenses.value = fetchedData.expenses;
      totalExpenses.value = fetchedData.total;
    }
    catch (error) {
      console.error(`An error has occured while fetching categories data: ${error}`);
    }
  }

  const fetchExpensesByMethod = async (user_id: number, month: string) => {
    try {
      const url = new URL("http://localhost:8000/transactions/fetch_by_method");
      url.searchParams.append("user_id", user_id.toString());
      url.searchParams.append("month", month);
      
      const response = await fetch(url.toString());

      if (!response.ok) {
        throw new Error (`HTTP error! Status: ${response.status}`);
      }
      const fetchedData = await response.json();
      expenses.value = fetchedData.expenses;
      totalExpenses.value = fetchedData.total;
    }
    catch (error) {
      console.error(`An error has occured while fetching categories data: ${error}`);
    }
  }

  return {
    transactionsData,
    errorMsg,
    loading,
    expenses,
    totalExpenses,
    fetchTransactions,
    deleteTransaction,
    fetchRecentTransactions,
    postNewExpenditure,
    fetchExpensesByCategory,
    fetchExpensesByMethod
  }
}