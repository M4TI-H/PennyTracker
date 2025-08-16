<script setup lang="ts">
import { Pie } from 'vue-chartjs'
import { Chart as ChartJS, Title, Tooltip, Legend, ArcElement } from 'chart.js'
import { computed, onMounted } from 'vue';
import type { BudgetSummary } from '@/types/budgets';

ChartJS.register(Title, Tooltip, Legend, ArcElement);

const { budgetSummaryData } = defineProps<{
  budgetSummaryData: BudgetSummary[]
}>();

const colors = ["#797d62", "#9b9b7a", "#d9ae94", "#f1dca7", "#ffcb69", "#d08c60", "#997b66", "#b5b8a3"];

const getData = computed(() => {
  if (!budgetSummaryData) return { labels: [], datasets: [] }
  
  const labels: string[] = [];
  const data: number[] = [];
  const backgroundColor: string[] = [];

  let remainingBudget = 0;

  budgetSummaryData.forEach((item, index) => {
    labels.push(`${item.name} spent`);
    data.push(item.amount_spent);
    backgroundColor.push(colors[index % colors.length]);

    remainingBudget += Math.max(item.total_budget - item.amount_spent, 0);
  })

  if (remainingBudget > 0) {
    labels.push("Not spent yet");
    data.push(remainingBudget);
    backgroundColor.push("#E0E0E0");
  }

  return {
    labels,
    datasets: [{
      data,
      backgroundColor,
      borderWidth: 0
    }]
  }
})

const options = {
  responsive: true,
  plugins: {
    legend: {
      display: false
    }
  }
}

</script>

<template>
  <Pie :data="getData" :options="options"/>
</template>