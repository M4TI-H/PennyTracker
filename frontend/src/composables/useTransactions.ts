import { ref } from "vue";
import type { Transaction, NewTransaction, Expense, MonthlyTransactions, TransactionCountType } from "@/types/transactions";
import formatDate from "./formatDate";
import { fetchData } from "./useFetchData";

export default function useTransactions() {
  const errorMsg = ref<string>("");
  const loading = ref<boolean>(false);

  const transactionsData = ref<Transaction[]>([]);
  // fetch all transactions
  const fetchTransactions = async() => {
    loading.value = true;

    const { data, error } = await fetchData<Transaction[]>("http://localhost:8000/transactions/fetch_all");
    if (error) errorMsg.value = error;
    else transactionsData.value = data ?? [];

    loading.value = false;
  }

  // fetch only few recent transactions
  const fetchRecentTransactions = async() => {
    loading.value = true;

    const { data, error } = await fetchData<Transaction[]>("http://localhost:8000/transactions/fetch_recent");
    if (error) errorMsg.value = error;
    else transactionsData.value = data ?? [];

    loading.value = false;
  }

  // delete transaction from history
  const deleteTransaction = async(user_id: number, transaction: number) => {
    loading.value = true;

    const url = new URL("http://localhost:8000/transactions/delete_one");
    url.searchParams.append("user_id", user_id.toString());
    url.searchParams.append("transaction_id", transaction.toString());

    const { error } = await fetchData<Transaction>(url.toString(), {
      method: "DELETE"
    });
    if (error) errorMsg.value = error;

    loading.value = false;
  }

  // add new transaction
  const postNewExpenditure = async(newExpData: NewTransaction, user_id: number) => {
    loading.value = true;

    const { error } = await fetchData<NewTransaction>("http://localhost:8000/transactions/new_expenditure/", {
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

    if (error) errorMsg.value = error;

    loading.value = false;
  }

  const expenses = ref<Expense[]>([]);
  const totalExpenses = ref<number>(0);
  // data used to display chart of summarized transactions by categories
  const fetchExpensesByCategory = async (user_id: number, month: string) => {
    loading.value = true;

    const url = new URL("http://localhost:8000/transactions/fetch_by_category");
    url.searchParams.append("user_id", user_id.toString());
    url.searchParams.append("month", month);
    
    let fetchedData: any = [];

    const { data, error } = await fetchData<Transaction[]>(url.toString());
    if (error) errorMsg.value = error;
    else fetchedData = data ?? [];

    expenses.value = fetchedData.expenses;
    totalExpenses.value = fetchedData.total;

    loading.value = false;
  }

  // data used to display chart of summarized transactions by methods
  const fetchExpensesByMethod = async (user_id: number, month: string) => {
    loading.value = true;

    const url = new URL("http://localhost:8000/transactions/fetch_by_method");
    url.searchParams.append("user_id", user_id.toString());
    url.searchParams.append("month", month);

    let fetchedData: any = [];

    const { data, error } = await fetchData<Transaction[]>(url.toString());
    if (error) errorMsg.value = error;
    else fetchedData = data ?? [];

    expenses.value = fetchedData.expenses;
    totalExpenses.value = fetchedData.total;

    loading.value = false;
  }

  const monthlyTransactionsData = ref<MonthlyTransactions[]>([]);
  const fetchMonthlyTransactions = async (user_id: number) => {
    loading.value = true;

    const url = new URL("http://localhost:8000/transactions/monthly_transactions/");
    url.searchParams.append("user_id", user_id.toString());
    
    const { data, error } = await fetchData<MonthlyTransactions[]>(url.toString());
    if (error) errorMsg.value = error;
    else monthlyTransactionsData.value = data ?? [];

    loading.value = false;
  }

  const transactionCount = ref<TransactionCountType[]>([]);
  // get number of transactions
  const fetchTransactionsCount = async (user_id: number) => {
    loading.value = true;

    const url = new URL("http://localhost:8000/transactions/transactions_count/");
    url.searchParams.append("user_id", user_id.toString());
    
    const { data, error } = await fetchData<TransactionCountType[]>(url.toString());
    if (error) errorMsg.value = error;
    else transactionCount.value = data ?? [];

    loading.value = false;
  }

  const months = ref<string[]>([]);
  //fetch names of months with transactions
  const fetchTransactionMonths = async (user_id: number) => {
    loading.value = true;

    const url = new URL("http://localhost:8000/transactions/transactions_months/");
    url.searchParams.append("user_id", user_id.toString());
    const { data, error} = await fetchData<string[]>(url.toString());
    if (error) errorMsg.value = error;
    else months.value = data ?? [];

    loading.value = false;
  }

  return {
    transactionsData,
    expenses,
    totalExpenses,
    monthlyTransactionsData,
    transactionCount,
    months,
    errorMsg,
    loading,
    fetchTransactions,
    deleteTransaction,
    fetchRecentTransactions,
    postNewExpenditure,
    fetchExpensesByCategory,
    fetchExpensesByMethod,
    fetchMonthlyTransactions,
    fetchTransactionsCount,
    fetchTransactionMonths
  }
}