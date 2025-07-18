<script setup lang="ts">
import type { TransactionsChart } from "@/types/transactions";
import { Bar } from 'vue-chartjs'
import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale } from 'chart.js'
import { computed } from "vue";

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale)

const { chartData } = defineProps<{
  chartData: TransactionsChart
}>();

const colors = ["#a3b18a", "#588157", "#3A5A40"]

const data = computed(() => ({
  labels: chartData.month,
  datasets: [{
    label: "Total expenses",
    data: chartData.total_expenses,
    backgroundColor: chartData.month.map((_, i) => colors[i % colors.length])
  }]
}));

const options = {
  responsive: true,
  scales: {
    y: {
      beginAtZero: true
    }
  }
};

</script>

<template>
  <Bar :data="data" :options="options" />
</template>