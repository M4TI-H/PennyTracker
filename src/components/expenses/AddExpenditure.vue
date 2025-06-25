<script setup>
defineProps({
  expenseCategories: Array,
  paymentMethods: Array
})
</script>

<template>
  <div class="w-[25%] flex flex-col items-center gap-6">
    <p class="text-2xl text-neutral-800 font-semibold">New expenditure</p>
    <input type="text" placeholder="Name of expense" class="w-[70%] h-10 bg-[#FFF] border-2 border-neutral-800 rounded-lg font-semibold text-md px-2 focus:outline-0"/>
    <input type="number" placeholder="Amount" class="w-[70%] h-10 bg-[#FFF] border-2 border-neutral-800 rounded-lg font-semibold text-md px-2 focus:outline-0"/>
    <span class="w-[70%] h-10 flex justify-between items-center pl-2">
      <p class="text-md text-neutral-800 font-semibold">Method:</p>
      <select class="w-40 h-10 bg-[#FFF] border-2 border-neutral-800 rounded-lg font-semibold text-md px-2 focus:outline-0">
        <option v-for="method in paymentMethods" :key="new Date()">{{ method }}</option>
      </select>
    </span>
    <span class="w-[70%] h-10 flex justify-between items-center pl-2">
      <p class="text-md text-neutral-800 font-semibold">Category:</p>
      <select class="w-40 h-10 bg-[#FFF] border-2 border-neutral-800 rounded-lg font-semibold text-md px-2 focus:outline-0">
        <option v-for="category in expenseCategories" :key="new Date()">{{ category }}</option>
      </select>
    </span>
    <button class="w-[50%] h-10 rounded-3xl bg-neutral-800 text-sm text-[#E9ECEF]
    border-neutral-800 border-2 hover:cursor-pointer hover:bg-[#588157]
      transition ease-in-out duration-200">Confirm</button>
  </div>
</template>