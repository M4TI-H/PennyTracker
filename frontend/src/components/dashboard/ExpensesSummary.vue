<script setup lang="ts">
import { onMounted, ref, computed, watch } from "vue";
import type { MonthlyTransactions, TransactionsChart } from "@/types/transactions";
import { fetchTransactionsMonthly } from "@/composables/dashboardDataFetches";
import MonthlyExpensesChart from "./MonthlyExpensesChart.vue";

const monthlyTransactionsData = ref<MonthlyTransactions[]>([]);
const chartData = ref<TransactionsChart>({
  month: [],
  total_expenses: [],
  number_of_transactions: []
});

function formatDate(date: string) {
  const [year, month] = date.split("-");
  const formattedDate = new Date(Number(year), parseInt(month, 10) - 1);
  return formattedDate.toLocaleString("en-US", { month: "long", year: "numeric" });
}

onMounted(async() => {
  monthlyTransactionsData.value = await fetchTransactionsMonthly(2);
});

watch(monthlyTransactionsData, (newValue) => {
  chartData.value = {
    month: newValue.map(m => formatDate(m.month)),
    total_expenses: newValue.map(m => m.total_expenses),
    number_of_transactions: newValue.map(m => m.number_of_transactions)
  };
});

</script>

<template>
  <div class="w-full sm:w-[60%] max-h-[45%] min-h-32 h-full sm:h-96 bg-[#E9ECEF] p-4 rounded-xl shadow-xl
    flex flex-col items-center"
  >
    <MonthlyExpensesChart :chartData="chartData"/>
  </div>
</template>