<script setup lang="ts">
import { ref, onMounted } from "vue";
import Navigation from "@/components/navigation/Navigation.vue";
import useScreenSize from "@/composables/screenSize.ts";
import BudgetSection from "@/components/budget/BudgetSection.vue";

const smallW = 640;
const {screenWidth, screenHeight} = useScreenSize();

</script>

<template>
  <div class="fixed flex w-full h-full justify-around bg-[#444] sm:py-16 ">
    <Navigation v-if="screenWidth >= smallW" :screenWidth="screenWidth"/>

    <span class="w-[96rem] flex flex-row flex-wrap items-start gap-8">
      <BudgetSection />
      <div class="w-[35%] h-full flex flex-col gap-4">
        <div class="h-full w-full bg-[#E9ECEF] flex flex-col p-4
          rounded-xl shadow-xl">
          <p class="text-3xl text-[#212529] font-semibold">nwm co</p>
        </div>
      </div>
    </span>
  </div>
</template>