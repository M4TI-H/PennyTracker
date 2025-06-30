<script setup>
defineProps({
  transactionsData: Array
});
</script>

<template>
  <div class="w-full h-8 flex items-center">
    <p class="w-[15%] text-md text-neutral-800 font-bold">Amount</p>
    <p class="w-[30%] text-md text-neutral-800 font-bold">Title</p>
    <p class="w-[25%] text-md text-neutral-800 font-bold">Category</p>
    <p class="w-[15%] text-md text-neutral-800 font-bold">Method</p>
    <p class="w-[15%] text-md text-neutral-800 font-bold">Date</p>
  </div>
  <div v-for="expense in transactionsData" :key="expense.id" class="w-full h-8 flex items-center">
    <p class="w-[15%] text-sm text-neutral-800 font-semibold">${{ expense.amount }}</p>
    <p class="w-[30%] text-sm text-neutral-800 font-semibold">{{ expense.name }}</p>
    <p class="w-[25%] text-sm text-neutral-800 font-semibold">{{ expense.category_name }}</p>
    <p class="w-[15%] text-sm text-neutral-800 font-semibold">{{ expense.method }}</p>
    <p class="w-[15%] text-sm text-neutral-800 font-semibold">{{ expense.date }}</p>
  </div>
</template>