<script setup>
defineProps({
  account: String,
  balance: String
})
</script>

<template>
  <div class="max-w-[50%] w-full h-24 sm:h-32 bg-[#E9ECEF] flex flex-col p-4
    rounded-xl shadow-xl 
    hover:scale-102 hover:cursor-pointer hover:bg-[#DEE2E6]
    transition ease-in-out duration-200">
    <p class="text-md sm:text-xl text-[#212529] font-semibold">{{ account }}</p>
    <span class="flex items-end">
      <p class="text-2xl sm:text-4xl text-[#212529] font-bold mt-4">${{ balance.substr(0, balance.length-3) }}</p>
      <p class="text-md sm:text-xl text-[#212529] font-semibold mt-4">{{ balance.substr(-3) }}</p>
    </span>
  </div>
</template>