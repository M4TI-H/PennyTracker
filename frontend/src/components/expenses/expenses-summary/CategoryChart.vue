<script setup lang="ts">
import { Bar } from 'vue-chartjs'
import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale } from 'chart.js'
import { computed } from "vue";
import type { ExpenseChart } from '@/types/transactions';

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale)

const { chartData } = defineProps<{
  chartData: ExpenseChart
}>();

const colors = ["#a3b18a", "#588157", "#3A5A40"]

const data = computed(() => ({
  labels: chartData.category,
  datasets: [{
    label: "Expenses by category",
    data: chartData.total,
    backgroundColor: chartData.category.map((_, i) => colors[i % colors.length])
  }]
}));

const options = {
  responsive: true,
  scales: {
    y: {
      beginAtZero: true,
      title: {
        display: true,
        text: "Total expenses ($)"
      }
    },
    x: {
      title: {
        display: true,
        text: "Expense category"
      }
    }
  }
};

</script>

<template>
  <Bar :data="data" :options="options" />
</template>