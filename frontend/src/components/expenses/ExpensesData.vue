<script setup>
defineProps({
  expenses: Array,
  filter: String
});

</script>

<template>
  <span v-if="filter === 'category'" v-for="expense in expenses" :key="expense.category" class=" w-[50%] flex flex-col pl-8">
    <p class="text-lg text-neutral-800 font-semibold mt-2">
      {{ expense.category }}: ${{ expense.total }}
    </p>
    <p class="text-md text-neutral-800 ml-2" v-for="(amount, method) in expense.method">
      {{ method }} - ${{ amount }}
    </p>
  </span>

  <span v-else-if="filter === 'method'" v-for="expense in expenses" :key="expense.method" class=" w-[50%] flex flex-col pl-8">
    <p class="text-lg text-neutral-800 font-semibold mt-2">
      {{ expense.method }}: ${{ expense.total }}
    </p>
    <p class="text-md text-neutral-800 ml-2" v-for="(amount, method) in expense.category">
      {{ method }} - ${{ amount }}
    </p>
  </span>
</template>