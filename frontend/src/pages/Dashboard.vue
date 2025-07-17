<script setup lang="ts">
// @ts-nocheck
import { ref, watchEffect, onMounted } from "vue";
import Navigation from "@/components/navigation/Navigation.vue";
import CompactNavigation from "@/components/navigation/CompactNavigation.vue";
import NameCard from "@/components/dashboard/NameCard.vue";
import PiggyBank from "@/components/dashboard/PiggyBank.vue";
import ExpensesSummary from "@/components/dashboard/ExpensesSummary.vue";
import AccountView from "@/components/options/AccountView.vue";
import fetchAccounts from "@/composables/fetchAccounts";
import useScreenSize from "@/composables/screenSize";
import TransactionCount from "@/components/dashboard/TransactionCount.vue";

const smallW = 640;
const {screenWidth, screenHeight}: {screenWidth: number, screenHeight: number} = useScreenSize();

const totalMonthlySavings = ref(0);
const month = ref("");

const fetchTotalMonthlySavings = async (user_id, month) => {
  try {
    const url = new URL("http://localhost:8000/savings/this_month_sum/");
    url.searchParams.append("user_id", user_id);
    url.searchParams.append("month", month);
    
    const response = await fetch(url.toString());

    if (!response.ok) {
      throw new Error (`HTTP error! Status: ${response.status}`);
    }

    totalMonthlySavings.value = await response.json();
  }
  catch (error) {
    console.error(`An error has occured while fetching savings data: ${error}`);
  }
}

const monthlyTransactionsData = ref([]);
const fetchTransactionsMonthly = async(user_id) => {
   try {
    const url = new URL("http://localhost:8000/transactions/monthly_transactions/");
    url.searchParams.append("user_id", user_id);
    
    const response = await fetch(url.toString());

    if (!response.ok) {
      throw new Error (`HTTP error! Status: ${response.status}`);
    }

    monthlyTransactionsData.value = await response.json();
  }
  catch (error) {
    console.error(`An error has occured while fetching transactions data: ${error}`);
  }
}

const transactionsCountData = ref([]);
const fetchTransactionsCount = async(user_id) => {
   try {
    const url = new URL("http://localhost:8000/transactions/transactions_count/");
    url.searchParams.append("user_id", user_id);
    
    const response = await fetch(url.toString());

    if (!response.ok) {
      throw new Error (`HTTP error! Status: ${response.status}`);
    }

    transactionsCountData.value = await response.json();
    transactionsCountData.value = transactionsCountData.value.map(t => {
      let level = 0;
      let num = t.number_of_transactions;
      if (num === 1){
        level = 1;
      }
      else if (num === 2 || num === 3) {
        level = 2;
      }
      else if (num > 3 && num <= 5) {
        level = 3;
      }
      else if (num > 5 && num < 10){
        level = 4;
      }
      
      return {...t, level};
    });
  }
  catch (error) {
    console.error(`An error has occured while fetching transactions data: ${error}`);
  }
}

onMounted(async() => {
  month.value = (new Date().getMonth() + 1).toString().padStart(2, "0");
  await fetchTotalMonthlySavings(2, month.value);
  await fetchTransactionsMonthly(2);
  await fetchTransactionsCount(2);
});

const accountsData = ref([]);
watchEffect(async () => {
  accountsData.value = await fetchAccounts(2);
});
</script>

<template>
  <div class="fixed flex w-full h-full justify-around bg-[#DAD7CD] sm:py-16 ">
    <!--Menu bar with buttons-->
    <Navigation v-if="screenWidth >= smallW" :screenWidth="screenWidth"/>
    <CompactNavigation v-else/>
    <!--Cards grid-->
    <span class="max-w-[96rem] p-2 sm:p-0 flex flex-col sm:flex-row sm:flex-wrap items-center sm:items-start gap-4">
      <div class="sm:min-w-96 sm:max-w-[40%] sm:w-[30%] min-h-[30%] max-h-[10%] w-full flex flex-col gap-4">
        <!--User welcome card-->  
        <NameCard />
        <span class="flex h-[55%] sm:h-32 gap-2">
          <AccountView v-for="account in accountsData" :key="account.id" :account="account" @delete="fetchAccounts(2)"/>
        </span>
      </div>
      <ExpensesSummary :monthlyTransactionsData="monthlyTransactionsData"/>
      <span class="flex w-[90%] max-h-[15%] sm:max-h-[50%] h-full gap-4">
        <TransactionCount :transactionsCountData="transactionsCountData" />
        <PiggyBank :screenWidth="screenWidth" :totalMonthlySavings="totalMonthlySavings"/>
      </span>
    </span>
  </div>
</template>