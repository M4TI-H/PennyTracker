<script setup lang="ts">
import { onMounted, ref, watch } from 'vue';
import ExpensesData from './ExpensesData.vue';
import type { Expense, ExpensesByCategoryChart, ExpensesByMethodChart } from '@/types/transactions';
import CategoryChart from './CategoryChart.vue';
import MethodChart from './MethodChart.vue';
import getMonthName from '@/composables/getMonthName';

const selectedFilter = ref<string>("category");
const expenses = ref<Expense[]>([]);
const totalExpenses = ref<number>(0.0);
const monthId = ref<string>("");

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

function getMonths(): { id: number; month_num: string; month_name: string, year: string }[] {
  const result: { id: number; month_num: string; month_name: string, year: string }[] = [];
  const now = new Date();

  for (let i = 0; i < 12; i++) {
    const date = new Date(now.getFullYear(), now.getMonth() - i, 1);
    const month_num = (date.getMonth() + 1).toString().padStart(2, "0");
    const month_name = getMonthName(month_num);
    const year = date.getFullYear().toString();
    result.push({id: i, month_num, month_name, year});
  }

  return result;
}

watch([monthId, selectedFilter], async ([newMonth, newFilter]) => {
  if (newFilter === "category") await fetchExpensesByCategory(2, newMonth);
  else if (newFilter === "method") await fetchExpensesByMethod(2, newMonth);
});

const refreshData = async () => {
  if (selectedFilter.value === "category") await fetchExpensesByCategory(2, monthId.value);
  else if (selectedFilter.value === "method") await fetchExpensesByMethod(2, monthId.value);
};

const categoryChartData = ref<ExpensesByCategoryChart>({
  category: [],
  method: [],
});

const methodChartData = ref<ExpensesByMethodChart>({
  category: [],
  method: [],
});

watch(expenses, (newValue) => {
  if (selectedFilter.value === "category") {
    categoryChartData.value = {
      category: newValue.map(e => e.category),
      method: newValue.map(e => e.method),
    };
  } 
  else if (selectedFilter.value === "method") {
    methodChartData.value = {
      method: newValue.map(e => e.method),
      category: newValue.map(e => e.category),
    };
  }
});

defineExpose({
  refreshData
});

onMounted(async () => {
  monthId.value = (new Date().getMonth() + 1).toString().padStart(2, "0");
  refreshData();
});

</script>

<template>
  <div class="w-full h-full p-2 flex justify-evenly">
    <div class="w-[25%] h-full">
      <span class="flex items-center gap-4">
        <p class="text-lg text-neutral-800 font-semibold">Your expenses in</p>
        <select v-model="monthId"
          class="w-35 h-10 bg-[#FFF] border-2 border-neutral-800 rounded-lg font-semibold text-md px-2 focus:outline-0"
        >
          <option v-for="month in getMonths()" :key="month.id" :value="month.month_num">
            {{ month.month_name }} ({{ month.year }})
          </option>
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
      <p v-if="totalExpenses" class="text-lg text-neutral-800 font-semibold ml-8 mt-2">Total: ${{ totalExpenses.toFixed(2) }}</p>
      <p v-else class="text-lg text-neutral-800 font-semibold ml-8 mt-2">No data</p>
    </div>
    <div class="w-198 h-full">
      <CategoryChart v-if="selectedFilter === 'category'" :chartData="categoryChartData"/>
      <MethodChart v-else-if="selectedFilter === 'method'" :chartData="methodChartData"/>
    </div>
  </div>
</template>