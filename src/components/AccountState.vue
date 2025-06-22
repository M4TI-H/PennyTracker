<script setup>
defineProps({
  account: String,
  balance: String`1`
})
</script>

<template>
  <div class="w-60 h-32 bg-[#E9ECEF] flex flex-col p-4
    rounded-xl shadow-xl">
    <p class="text-xl text-[#212529] font-semibold">{{ account }}</p>
    <span class="flex items-end">
      <p class="text-4xl text-[#212529] font-bold mt-4">${{ balance.substr(0, balance.length-3) }}</p>
      <p class="text-xl text-[#212529] font-semibold mt-4">{{ balance.substr(-3) }}</p>
    </span>
  </div>
</template>