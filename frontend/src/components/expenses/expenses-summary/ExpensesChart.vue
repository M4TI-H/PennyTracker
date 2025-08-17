<script setup lang="ts">
import { onMounted, ref, watch } from 'vue';
import ExpensesData from './ExpensesData.vue';
import type { ExpensesByCategoryChart, ExpensesByMethodChart } from '@/types/transactions';
import CategoryChart from './CategoryChart.vue';
import MethodChart from './MethodChart.vue';
import getMonthName from '@/composables/getMonthName';
import useTransactions from '@/composables/useTransactions';

const selectedFilter = ref<string>("category");
const monthId = ref<string>("");

const { expenses, totalExpenses, fetchExpensesByCategory, fetchExpensesByMethod, months, fetchTransactionMonths } = useTransactions();

function getMonths(): { month_num: string; month_name: string, year: string }[] {
  const result: { month_num: string; month_name: string, year: string }[] = [];

  for (let month of months.value) {
    const month_num = month.slice(0, 2);
    const month_name = getMonthName(month_num);
    const year = month.slice(3, 7);
    result.push({month_num, month_name, year});
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
  method: []
});

const methodChartData = ref<ExpensesByMethodChart>({
  method: [],
  category: []
});

watch(expenses, (newValue) => {
  if (selectedFilter.value === "category") {
    categoryChartData.value = {
      category: newValue.map(e => e.category),
      method: newValue.map(e => e.method)
    };
  } 
  else if (selectedFilter.value === "method") {
    methodChartData.value = {
      method: newValue.map(e => e.method),
      category: newValue.map(e => e.category)
    };
  }
});

defineExpose({
  refreshData
});

onMounted(async () => {
  monthId.value = (new Date().getMonth() + 1).toString().padStart(2, "0");
  refreshData();
  await fetchTransactionMonths(2);
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
          <option v-for="(month, id) in getMonths()" :key="id" :value="month.month_num">
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