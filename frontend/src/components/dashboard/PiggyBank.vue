<script setup lang="ts">
import { ref, onMounted } from "vue";
import useScreenSize from "@/composables/screenSize.ts";
import { fetchTotalMonthlySavings } from "@/composables/dashboardDataFetches";

const {screenWidth, screenHeight} = useScreenSize();
const totalMonthlySavings = ref<number>(0);
const month = ref<string>("");

onMounted(async() => {
  month.value = (new Date().getMonth() + 1).toString().padStart(2, "0");
  totalMonthlySavings.value = await fetchTotalMonthlySavings(2, month.value);
})

</script>

<template>
  <div class="relative max-w-[50%] min-w-36 sm:min-w-64 sm:max-w-[35%] w-full sm:h-96 
    flex flex-col items-center justify-center bg-[#E9ECEF] rounded-xl shadow-xl"
  >
    <p v-if="screenWidth > 640" class="text-md sm:text-3xl text-[#212529] font-semibold">Savings this month</p>
    <img src="https://www.iconpacks.net/icons/1/free-piggy-bank-icon-942-thumb.png"
      class="size-32 sm:size-72"
    />
    <p class="absolute top-2/5 sm:top-3/7 text-2xl sm:text-5xl text-[#212529] font-semibold">${{ totalMonthlySavings }}</p>
    <a href="/savings" v-if="screenWidth > 640" class="text-lg text-[#212529] font-semibold
      hover:underline hover:cursor-pointer"
    >See more</a>
  </div>
</template>