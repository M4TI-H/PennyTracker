<script setup>
  let monthNow = new Date().toLocaleString("en-GB", { month: "long"});
</script>

<template>
  <div class="w-full sm:w-[60%] max-h-[45%] min-h-32 h-full sm:h-96 bg-[#E9ECEF] p-4 rounded-xl shadow-xl
    flex flex-col items-center"
  >
    <span class="flex">
      <p class="text-lg sm:text-3xl text-[#212529] font-semibold">Your expenses in {{ monthNow }}</p>
    </span>
  </div>
</template>