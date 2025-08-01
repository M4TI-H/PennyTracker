<script setup lang="ts">
import { ref, onMounted } from "vue";
import Navigation from "@/components/navigation/Navigation.vue";
import useScreenSize from "@/composables/useScreenSize";
import BudgetSection from "@/components/budget/BudgetSection.vue";
import BudgetDistribution from "@/components/budget/BudgetDistribution.vue";

const smallW = 640;
const {screenWidth, screenHeight} = useScreenSize();

</script>

<template>
  <div class="fixed flex w-full h-full justify-around bg-[#444] sm:py-16 ">
    <Navigation v-if="screenWidth >= smallW" :screenWidth="screenWidth"/>
    <span class="w-[96rem] flex flex-row flex-wrap items-start gap-8">
      <BudgetSection />
      <BudgetDistribution />
    </span>
  </div>
</template>