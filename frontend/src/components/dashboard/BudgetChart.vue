<script setup lang="ts">
import getMonthName from "@/composables/getMonthName";
import BudgetChartDetailed from "../budget/BudgetChartDetailed.vue";
import { onMounted } from "vue";
import useBudget from "@/composables/useBudget";

const { budgetSummaryData, budgetData, fetchBudget, fetchBudgetSummary } = useBudget();

onMounted(async () => {
  const now = new Date();
  const current = `${now.getFullYear()}-${(now.getMonth() + 1).toString().padStart(2, "0")}`;

  await fetchBudget(2, current);
  if (!budgetData.value?.id) return;
  await fetchBudgetSummary(budgetData.value.id);
});


</script>

<template>
   <div class="max-w-[30%] min-w-64 w-full h-96 flex flex-col items-center p-4
    bg-[#E9ECEF] rounded-xl shadow-xl">
    <p class="text-neutral-800 text-2xl font-semibold">Your budget in {{ getMonthName((new Date().getMonth() + 1).toString()) }}</p>
    <div class="w-[60%] h-full flex items-center justify-center">
      <BudgetChartDetailed v-if="budgetData" :budgetData="budgetData" :budgetSummaryData="budgetSummaryData"/>
    </div>
    <p class="text-neutral-800 text-lg font-semibold">Total budget: ${{ budgetData?.amount }}</p>
  </div>
</template>