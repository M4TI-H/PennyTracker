<script setup>
import { onMounted, ref } from 'vue';

const expenses = ref([]);
const totalExpenses = ref(0.0);

const fetchExpensesByCategory = async (user, month) => {
  try {
    const url = new URL("http://localhost:8000/transactions/fetch_by_category");
    url.searchParams.append("user_id", user);
    url.searchParams.append("month", month);
    
    const response = await fetch(url.toString(), {
      method: "GET",
      headers: {
        'Content-Type': 'application/json'
      }
    });

    if (!response.ok) {
      throw new Error (`HTTP error! Status: ${response.status}`);
    }
    const fetchedData = await response.json();
    return fetchedData;
  }
  catch (error) {
    console.error(`An error has occured while fetching categories data: ${error}`);
  }
}

onMounted(async () => {
  const fetchedData = await fetchExpensesByCategory(2, "06");
  console.log(fetchedData);
  expenses.value = fetchedData.expenses;
  totalExpenses.value = fetchedData.total;
});
</script>

<template>
  <div class="w-full h-full p-2">
    <div class="w-[25%] h-full">
      <p v-for="expense in expenses" :key="expense.id"
        class="text-md text-neutral-800 font-semibold"
      >{{ expense.category }} - ${{ expense.amount }}</p>
      <p>Total: ${{ totalExpenses }}</p>
    </div>
  </div>
</template>