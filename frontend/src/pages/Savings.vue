<script setup>
  import { ref, watchEffect, onMounted } from "vue";
  import Navigation from "@/components/navigation/Navigation.vue";
  import CompactNavigation from "@/components/navigation/CompactNavigation.vue";
  import Goal from "@/components/savings/Goal.vue";
  import NewGoal from "@/components/savings/NewGoal.vue";

  const screenWidth = ref(window.innerWidth);
  const screenHeight = ref(window.innerHeight);
  const smallW = 640;

  watchEffect(async () => {
    const handleResize = () => screenWidth.value = window.innerWidth;
    window.addEventListener("resize", handleResize);
    return () => window.removeEventListener("resize", handleResize);
  });

  watchEffect(async() => {
    const handleResize = () => screenHeight.value = window.innerHeight;
    window.addEventListener("resize", handleResize);
    return () => window.removeEventListener("resize", handleResize);
  });

  const savingsData = ref([]);

const fetchSavings = async() => {
  try {
    const response = await fetch("http://localhost:8000/savings/fetch_all");
    if (!response.ok) {
      throw new Error (`HTTP error! Status: ${response.status}`);
    }

    savingsData.value = await response.json();
    console.table(savingsData.value);
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
  <div class="fixed flex w-full h-full justify-center gap-16 bg-[#DAD7CD] sm:py-16 ">
    <!--Menu bar with buttons-->
    <Navigation v-if="screenWidth >= smallW" :screenWidth="screenWidth"/>
    <CompactNavigation v-else/>

    <span class="max-w-[96rem] h-auto w-full flex flex-col sm:flex-row sm:flex-wrap gap-8">
      <Goal v-for="goal in savingsData" :goalTitle="goal.title" :coverImage="goal.cover"
        :currentAmount="goal.current_amount" :goalAmount="goal.goal_amount"
      />
      <NewGoal />
    </span>
    
  </div>
</template>