<script setup lang="ts">
import { ref, onMounted } from "vue";
import Navigation from "@/components/navigation/Navigation.vue";
import CompactNavigation from "@/components/navigation/CompactNavigation.vue";
import PiggyBank from "@/components/savings/PiggyBank.vue";
import Goal from "@/components/savings/Goal.vue";
import NewGoal from "@/components/savings/NewGoal.vue";
import useScreenSize from "@/composables/screenSize.ts";
import type { GoalType } from "@/types/savings";

const smallW = 640;
const {screenWidth, screenHeight} = useScreenSize();

const savingsData = ref<GoalType[]>([]);

const fetchSavings = async() => {
  try {
    const response = await fetch("http://localhost:8000/savings/fetch_all");
    if (!response.ok) {
      throw new Error (`HTTP error! Status: ${response.status}`);
    }

    savingsData.value = await response.json();
  }
  catch (error) {
    console.error(`An error has occured while fetching savings data: ${error}`);
  }
}

onMounted(async () => {
  fetchSavings();
});

</script>

<template>
  <div class="fixed flex w-full h-full justify-center gap-16 bg-[#DAD7CD] sm:py-16">
    <!--Menu bar with buttons-->
    <Navigation v-if="screenWidth >= smallW" :screenWidth="screenWidth"/>
    <CompactNavigation v-else/>
    <span class="max-w-[96rem] h-auto w-full flex flex-wrap sm:flex-row sm:flex-wrap gap-8 overflow-y-auto">
      <PiggyBank />
      <Goal v-for="goal in savingsData" :key="goal.id" :goal="goal" @refresh="fetchSavings"/>
      <NewGoal @post-goal="fetchSavings"/>
    </span>
  </div>
</template>