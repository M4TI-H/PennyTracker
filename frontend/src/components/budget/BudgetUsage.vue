<script setup lang="ts">
import type { BudgetSummary } from '@/types/budgets';

const { budgetSummaryData } = defineProps<{
  budgetSummaryData: BudgetSummary[]
}>();

const budgetUsage = ((category: BudgetSummary) => {
   return (category.amount_spent / category.total_budget * 100).toFixed(2);
});

</script>

<template>
  <div class="w-full h-24 flex flex-wrap justify-center items-center gap-8">
    <p v-for="category in budgetSummaryData" class="font-semibold">
      {{ category.name }} - ${{ category.amount_spent }} / ${{ category.total_budget }} - {{ category.amount_spent === 0 ? 0 : budgetUsage(category) }}%
    </p> 
  </div>
</template>