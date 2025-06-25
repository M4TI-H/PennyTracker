<template>
  <div class="w-[90%] sm:w-[60%] max-h-[45%] h-full min-h-32 sm:h-96 bg-[#E9ECEF] p-4 rounded-xl shadow-xl
    flex flex-col items-center"
  >
    <span class="flex w-full">
      <p class="text-lg sm:text-3xl text-[#212529] font-semibold">Your expenses in {{ new Date().toLocaleString("en-GB", { month: "long"}) }}</p>
    </span>
    <span class="flex justify-around w-full">
    </span>
  </div>
</template>