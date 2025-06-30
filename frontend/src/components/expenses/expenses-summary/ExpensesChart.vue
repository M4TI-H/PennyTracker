<script setup>
import { onMounted, ref, watch } from 'vue';
import ExpensesData from './ExpensesData.vue';

const selectedFilter = ref("category");

const expenses = ref([]);
const totalExpenses = ref(0.0);
const userId = 2;
const monthId = ref("");

const fetchExpensesByCategory = async (user, month) => {
  try {
    const url = new URL("http://localhost:8000/transactions/fetch_by_category");
    url.searchParams.append("user_id", user);
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

const fetchExpensesByMethod = async (user, month) => {
  try {
    const url = new URL("http://localhost:8000/transactions/fetch_by_method");
    url.searchParams.append("user_id", user);
    url.searchParams.append("month", month);
    
    const response = await fetch(url.toString());

    if (!response.ok) {
      throw new Error (`HTTP error! Status: ${response.status}`);
    }
    const fetchedData = await response.json();
    expenses.value = fetchedData.expenses;
    totalExpenses.value = fetchedData.total;
    console.log('Fetched expenses:', expenses.value);
    console.log('Total:', totalExpenses.value);
  }
  catch (error) {
    console.error(`An error has occured while fetching categories data: ${error}`);
  }
}

const months = [
  { id: "01", name: "January" },
  { id: "02", name: "February" },
  { id: "03", name: "March" },
  { id: "04", name: "April" },
  { id: "05", name: "May" },
  { id: "06", name: "June" },
  { id: "07", name: "July" },
  { id: "08", name: "August" },
  { id: "09", name: "September" },
  { id: "10", name: "October" },
  { id: "11", name: "November" },
  { id: "12", name: "December" }
];

onMounted(async () => {
  monthId.value = (new Date().getMonth() + 1).toString().padStart(2, "0");
  if (selectedFilter.value === "category") {
    await fetchExpensesByCategory(userId, monthId.value);
  } 
  else if (selectedFilter.value === "method") {
    await fetchExpensesByMethod(userId, monthId.value);
  }
});

watch([monthId, selectedFilter], async ([newMonth, newFilter]) => {
  if (newFilter === "category") {
    await fetchExpensesByCategory(userId, newMonth);
  } 
  else if (newFilter === "method") {
    await fetchExpensesByMethod(userId, newMonth);
  }
})

const refreshData = async () => {
  if (selectedFilter.value === "category") {
    await fetchExpensesByCategory(userId, monthId.value);
  } 
  else if (selectedFilter.value === "method") {
    await fetchExpensesByMethod(userId, monthId.value);
  }
};

defineExpose({
  refreshData
});

</script>

<template>
  <div class="w-full h-full p-2">
    <div class="w-[25%] h-full">
      <span class="flex items-center gap-4">
        <p class="text-lg text-neutral-800 font-semibold">Your expenses in</p>
        <select v-model="monthId"
          class="w-35 h-10 bg-[#FFF] border-2 border-neutral-800 rounded-lg font-semibold text-md px-2 focus:outline-0"
        >
          <option v-for="month in months" :key="month.id" :value="month.id">{{ month.name }}</option>
        </select>
      </span>
      <div class="flex gap-4 justify-center">
        <span class="flex items-center gap-1">
          <input type="radio" v-model="selectedFilter" value="category" id="filtercategory"/>
          <label for="filterCategory" class="text-sm text-neutral-800">Category of expense</label>
        </span>
        <span class="flex items-center gap-1">
          <input type="radio" v-model="selectedFilter" value="method" id="filterMethod"/>
          <label for="filterMethod" class="text-sm text-neutral-800">Payment method</label>
        </span>
      </div>
      <ExpensesData :expenses="expenses" :filter="selectedFilter"/>

      <p v-if="totalExpenses" class="text-lg text-neutral-800 font-semibold ml-8 mt-2">Total: ${{ totalExpenses }}</p>
      <p v-else class="text-lg text-neutral-800 font-semibold ml-8 mt-2">No data</p>
    </div>
  </div>
</template>