<script setup lang="ts">
const { account, balance } = defineProps<{
  account: string,
  balance: string
}>();
</script>

<template>
  <div class="min-w-28 max-w-[50%] w-full h-full flex flex-col p-4
    rounded-xl shadow-xl bg-[#E9ECEF]
    hover:scale-102 hover:cursor-pointer hover:bg-[#DEE2E6]
    transition ease-in-out duration-200">
    <p class="text-md sm:text-xl text-[#212529] font-semibold">{{ account }}</p>
    <span class="flex items-end">
      <p class="text-2xl sm:text-4xl text-[#212529] font-bold mt-4">${{ balance.slice(0, -3) }}</p>
      <p class="text-md sm:text-xl text-[#212529] font-semibold mt-4">{{ balance.slice(-3) }}</p>
    </span>
  </div>
</template>