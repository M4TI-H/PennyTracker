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
  <div class="w-full h-96">
    <p v-for="category in budgetSummaryData">{{ category.name }} - ${{ category.amount_spent }} / ${{ category.total_budget }} - {{ budgetUsage(category) }}%</p> 
  </div>
</template>