<script setup>
import { ref, watchEffect } from "vue";

defineProps({
  expenseCategories: Array
});

const transactionsData = ref([]);

const fetch_transactions = async() => {
  try {
    const response = await fetch("http://localhost:8000/transactions/fetch_recent");
    if (!response.ok) {
      throw new Error (`HTTP error! Status: ${response.status}`);
    }

    transactionsData.value = await response.json();
  }
  catch (error) {
    console.error(`An error has occured while fetching transactions data: ${error}`);
  }
}

defineExpose({
  fetch_transactions
});

watchEffect(async() => {
  fetch_transactions();
});

</script>

<template>
  <div class="sm:w-[59%] h-[38%] flex flex-col items-center bg-[#E9ECEF] p-4 rounded-xl shadow-xl">
    <p class="text-2xl text-neutral-800 font-semibold mb-2">Recent transactions</p>
    <div class="w-[90%] h-8 flex items-center">
      <p class="w-[15%] text-md text-neutral-800 font-bold">Amount</p>
      <p class="w-[30%] text-md text-neutral-800 font-bold">Title</p>
      <p class="w-[25%] text-md text-neutral-800 font-bold">Category</p>
      <p class="w-[15%] text-md text-neutral-800 font-bold">Method</p>
      <p class="w-[15%] text-md text-neutral-800 font-bold">Date</p>
    </div>
    <div v-for="expense in transactionsData" :key="expense.id" class="w-[90%] h-8  flex items-center">
      <p class="w-[15%] text-sm text-neutral-800 font-semibold">${{ expense.amount }}</p>
      <p class="w-[30%] text-sm text-neutral-800 font-semibold">{{ expense.name }}</p>
      <p class="w-[25%] text-sm text-neutral-800 font-semibold">{{ expense.category_name }}</p>
      <p class="w-[15%] text-sm text-neutral-800 font-semibold">{{ expense.method }}</p>
      <p class="w-[15%] text-sm text-neutral-800 font-semibold">{{ expense.date }}</p>
    </div>
  </div>
</template>