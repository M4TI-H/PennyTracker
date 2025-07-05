<script setup>
import { ref, watchEffect } from "vue";
import Navigation from "../components/navigation/Navigation.vue";
import CompactNavigation from "../components/navigation/CompactNavigation.vue";
import AddExpenditure from "../components/expenses/expenses-summary/AddExpenditure.vue";
import Subscriptions from "../components/expenses/subscriptions/Subscriptions.vue";
import RecentTransactions from "../components/expenses/transaction-history/RecentTransactions.vue";
import AllTransactions from "../components/expenses/transaction-history/AllTransactions.vue";
import ExpensesChart from "../components/expenses/expenses-summary/ExpensesChart.vue";
import useScreenSize from "@/composables/screenSize";

const smallW = 640;
const {screenWidth, screenHeight} = useScreenSize();

const showAllExpenses = ref(false);
const expenseCategories = ref([]);
const accountsData = ref([]);

const fetchExpenseCategories = async() => {
  try {
    const response = await fetch("http://localhost:8000/transactions/expense_categories");
    if (!response.ok) {
      throw new Error (`HTTP error! Status: ${response.status}`);
    }
    expenseCategories.value = await response.json();
  }
  catch (error) {
    console.error(`An error has occured while fetching categories data: ${error}`);
  }
}

const fetchAccounts = async(user) => {
  try {
    const url = new URL("http://localhost:8000/transactions/fetch_accounts");
    url.searchParams.append("user_id", user);
    
    const response = await fetch(url.toString());

    if (!response.ok) {
      throw new Error (`HTTP error! Status: ${response.status}`);
    }
    accountsData.value = await response.json();
  }
  catch (error) {
    console.error(`An error has occured while fetching accounts data: ${error}`);
  }
}

const recentTransactionsComponent = ref(null);
const transactionsByCategory = ref(null);
const refreshTransactions = () => {
  recentTransactionsComponent.value?.fetchRecentTransactions();
  transactionsByCategory.value?.refreshData();
};

watchEffect(() => {
  fetchExpenseCategories(),
  fetchAccounts(2)
});
</script>
<template>
  <div class="fixed flex w-full h-full justify-center gap-16 bg-[#DAD7CD] sm:py-16 ">
    <!--Menu bar with buttons-->
    <Navigation v-if="screenWidth >= smallW" :screenWidth="screenWidth"/>
    <CompactNavigation v-else/>
    <span class="max-w-[96rem] h-auto w-full flex flex-col sm:flex-row sm:flex-wrap items-center justify-between sm:items-start">
      <div class="sm:max-w-[100%] w-full sm:min-w-128 sm:h-[54%] flex items-center bg-[#E9ECEF] p-4 rounded-xl shadow-xl">
        <AddExpenditure :expenseCategories="expenseCategories" :accountsData="accountsData" @after-submit="refreshTransactions"/>
        <div class="ml-4 w-[3px] h-[96%] bg-neutral-300"></div>
        <ExpensesChart ref="transactionsByCategory"/>
      </div>
      <!--Recent transactions section-->
      <RecentTransactions ref="recentTransactionsComponent" v-model="showAllExpenses" @deletion="refreshTransactions"/>
      <!--Subsription management-->
      <Subscriptions />
    </span>
  </div>
  <AllTransactions v-if="showAllExpenses" v-model="showAllExpenses" @deletion="refreshTransactions"/>
</template>