<script setup lang="ts">
import getMonthName from "@/composables/getMonthName";

</script>

<template>
   <div class="max-w-[30%] min-w-64 w-full h-96 flex flex-col items-center p-4
    bg-[#E9ECEF] rounded-xl shadow-xl">
    <p class="text-neutral-800 text-2xl font-semibold">Your budget in {{ getMonthName((new Date().getMonth() + 1).toString()) }}</p>
  </div>
</template>