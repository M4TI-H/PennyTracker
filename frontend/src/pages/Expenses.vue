<script setup lang="ts">
import { onMounted, ref } from "vue";
import Navigation from "../components/navigation/Navigation.vue";
import AddExpenditure from "../components/expenses/expenses-summary/AddExpenditure.vue";
import Subscriptions from "../components/expenses/subscriptions/Subscriptions.vue";
import RecentTransactions from "../components/expenses/transaction-history/RecentTransactions.vue";
import AllTransactions from "../components/expenses/transaction-history/AllTransactions.vue";
import ExpensesChart from "../components/expenses/expenses-summary/ExpensesChart.vue";
import useScreenSize from "@/composables/useScreenSize";
import useExpenseCategories from "@/composables/useExpenseCategories.ts";
import useAccounts from "@/composables/useAccounts.ts";

const {screenWidth, screenHeight} = useScreenSize();

const showAllExpenses = ref(false);

const { expenseCategories, fetchActiveCategories } = useExpenseCategories();
const { accountsData, fetchActiveAccounts } = useAccounts();

const refreshData = async () => {
  await fetchActiveCategories(2);
  await fetchActiveAccounts(2);
}

type RecentTransactionsExpose = {
  fetchRecentTransactions: () => void;
};

type TransactionsByCategoryExpose = {
  refreshData: () => void;
};

const recentTransactionsComponent = ref<RecentTransactionsExpose | null>(null);
const transactionsByCategory = ref<TransactionsByCategoryExpose | null>(null);

const refreshTransactions = () => {
  recentTransactionsComponent.value?.fetchRecentTransactions();
  transactionsByCategory.value?.refreshData();
};

onMounted(async () => refreshData());

</script>
<template>
  <div class="fixed flex w-full h-full justify-center gap-16 bg-[#DAD7CD] sm:py-16 ">
    <!--Menu bar with buttons-->
    <Navigation :screenWidth="screenWidth"/>
    <span class="max-w-[96rem] h-auto w-full flex flex-col sm:flex-row sm:flex-wrap items-center justify-between sm:items-start">
      <div class="sm:max-w-[100%] w-full sm:min-w-128 sm:h-[54%] flex items-center bg-[#E9ECEF] p-4 rounded-xl shadow-xl">
        <AddExpenditure :expenseCategories="expenseCategories" :accountsData="accountsData" @submit="refreshTransactions"/>
        <div class="ml-4 w-[3px] h-[96%] bg-neutral-300"></div>
        <ExpensesChart ref="transactionsByCategory"/>
      </div>
      <!--Recent transactions section-->
      <RecentTransactions ref="recentTransactionsComponent" v-model:visible="showAllExpenses" @deletion="refreshTransactions"/>
      <!--Subsription management-->
      <Subscriptions />
    </span>
  </div>
  <AllTransactions v-if="showAllExpenses" v-model:visible="showAllExpenses" @deletion="refreshTransactions"/>
</template>