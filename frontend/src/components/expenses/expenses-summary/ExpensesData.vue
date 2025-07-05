<script setup>
defineProps({
  expenses: Array,
  filter: String
});

</script>
<template>
  <span v-if="filter === 'category'" v-for="expense in expenses" :key="expense.category" class=" w-full flex flex-col pl-8">
    <p class="text-lg text-neutral-800 font-semibold mt-2">
      {{ expense.category }}: ${{ parseFloat(expense.total).toFixed(2) }}
    </p>
    <p class="text-md text-neutral-800 ml-2" v-for="(amount, method) in expense.method">
      {{ method }} - ${{ parseFloat(amount).toFixed(2) }}
    </p>
  </span>

  <span v-else-if="filter === 'method'" v-for="expense in expenses" :key="expense.method" class=" w-full flex flex-col pl-8">
    <p class="text-lg text-neutral-800 font-semibold mt-2">
      {{ expense.method }}: ${{ parseFloat(expense.total).toFixed(2) }}
    </p>
    <p class="text-md text-neutral-800 ml-2" v-for="(amount, method) in expense.category">
      {{ method }} - ${{ parseFloat(amount).toFixed(2) }}
    </p>
  </span>
</template>