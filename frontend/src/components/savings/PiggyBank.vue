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
  <div class="relative w-172 h-64 flex flex-col items-center justify-center 
    bg-[#E9ECEF] rounded-xl shadow-xl"
  >
    <p v-if="screenWidth > 640" class="text-3xl text-[#212529] font-semibold">Total savings this month</p>
    <img src="https://www.iconpacks.net/icons/1/free-piggy-bank-icon-942-thumb.png"
      class="size-52"
    />
    <p class="absolute top-1/2 text-3xl text-[#212529] font-semibold">${{ totalMonthlySavings }}</p>
  </div>
</template>