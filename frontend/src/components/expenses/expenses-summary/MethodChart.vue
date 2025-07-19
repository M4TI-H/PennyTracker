<script setup lang="ts">
import { Bar } from 'vue-chartjs'
import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale } from 'chart.js'
import { computed } from "vue";
import type { ExpensesByMethodChart } from '@/types/transactions';

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale)

const { chartData } = defineProps<{
  chartData: ExpensesByMethodChart
}>();

const colors = ["#797d62", "#9b9b7a", "#d9ae94", "#f1dca7", "#ffcb69", "#d08c60", "#997b66", "#b5b8a3"];

function getData() {
  const categoriesSet = new Set<string>;

  for (const categoryObject of chartData.category){
    for (const category in categoryObject) {
      categoriesSet.add(category);
    }
  }

  const categories = Array.from(categoriesSet);
  const dataset: {label: string; data: number[], backgroundColor: string}[] = [];

  for (const [id, category] of categories.entries()) {
    const expenses: number[] = chartData.category.map(categoryObj => categoryObj[category] || 0);
    dataset.push({label: category, data: expenses, backgroundColor: colors[id % colors.length] })
  }

  return dataset;
}

const data = computed(() => ({
  labels: chartData.method,
  datasets: getData()
}));

const options = {
  responsive: true,
  scales: {
    x: {
      stacked: true,
      title: {
        display: true,
        text: "Payment method"
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