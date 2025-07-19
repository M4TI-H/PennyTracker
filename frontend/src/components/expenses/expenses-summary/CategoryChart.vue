<script setup lang="ts">
import { Bar } from 'vue-chartjs'
import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale } from 'chart.js'
import { computed } from "vue";
import type { ExpensesByCategoryChart } from '@/types/transactions';

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale)

const { chartData } = defineProps<{
  chartData: ExpensesByCategoryChart
}>();

const colors = ["#797d62", "#9b9b7a", "#d9ae94", "#f1dca7", "#ffcb69", "#d08c60", "#997b66", "#b5b8a3"];

function getData() {
  const methodsSet = new Set<string>;

  for (const methodObject of chartData.method){
    for (const method in methodObject) {
      methodsSet.add(method);
    }
  }

  const methods = Array.from(methodsSet);
  const dataset: {label: string; data: number[], backgroundColor: string}[] = [];

  for (const [id, method] of methods.entries()) {
    const expenses: number[] = chartData.method.map(methodObj => methodObj[method] || 0);
    dataset.push({label: method, data: expenses, backgroundColor: colors[id % colors.length] })
  }

  return dataset;
}

const data = computed(() => ({
  labels: chartData.category,
  datasets: getData()
}));

const options = {
  responsive: true,
  scales: {
    x: {
      stacked: true,
      title: {
        display: true,
        text: "Expense category"
      }
    },
    y: {
      stacked: true,
      beginAtZero: true,
      title: {
        display: true,
        text: "Total expenses ($)"
      }
    },
  }
};

</script>

<template>
  <Bar :data="data" :options="options" />
</template>