<script setup lang="ts">
import type { Expense } from '@/types/transactions';

const { expenses, filter } = defineProps<{
  expenses: Expense[],
  filter: string
}>();

</script>
<template>
  <span v-if="filter === 'category'" v-for="expense in expenses" :key="expense.category" class=" w-full flex flex-col pl-8">
    <p class="text-lg text-neutral-800 font-semibold mt-2">
      {{ expense.category }}: ${{ expense.total.toFixed(2) }}
    </p>
    <p class="text-md text-neutral-800 ml-2" v-for="(amount, method) in expense.method">
      {{ method }} - ${{ Number(amount).toFixed(2) }}
    </p>
  </span>

  <span v-else-if="filter === 'method'" v-for="(expense, id) in expenses" :key="id" class=" w-full flex flex-col pl-8">
    <p class="text-lg text-neutral-800 font-semibold mt-2">
      {{ expense.method }}: ${{ expense.total.toFixed(2) }}
    </p>
    <p class="text-md text-neutral-800 ml-2" v-for="(amount, method) in expense.category">
      {{ method }} - ${{ Number(amount).toFixed(2) }}
    </p>
  </span>
</template>