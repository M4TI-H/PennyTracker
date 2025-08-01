<script setup lang="ts">
import { onMounted } from "vue";
import Navigation from "@/components/navigation/Navigation.vue";
import PiggyBank from "@/components/savings/PiggyBank.vue";
import Goal from "@/components/savings/Goal.vue";
import NewGoal from "@/components/savings/NewGoal.vue";
import useScreenSize from "@/composables/useScreenSize";
import useSavings from "@/composables/useSavings";

const {screenWidth, screenHeight} = useScreenSize();

const { savingsData, fetchGoals } = useSavings();

onMounted(async () => {
  fetchGoals();
});

</script>

<template>
  <div class="fixed flex w-full h-full justify-center gap-16 bg-[#DAD7CD] sm:py-16">
    <!--Menu bar with buttons-->
    <Navigation :screenWidth="screenWidth"/>
    <span class="max-w-[96rem] h-auto w-full flex flex-wrap sm:flex-row sm:flex-wrap gap-8 overflow-y-auto">
      <PiggyBank @refresh="fetchGoals"/>
      <Goal v-for="goal in savingsData" :key="goal.id" :goal="goal" @refresh="fetchGoals"/>
      <NewGoal @post-goal="fetchGoals"/>
    </span>
  </div>
</template>