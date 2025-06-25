<script setup>
  import { ref, watchEffect } from "vue";
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
</script>

<template>
  <div class="fixed flex w-full h-full justify-center gap-16 bg-[#DAD7CD] sm:py-16 ">
    <!--Menu bar with buttons-->
    <Navigation v-if="screenWidth >= smallW" :screenWidth="screenWidth"/>
    <CompactNavigation v-else/>

    <span class="max-w-[96rem] h-auto w-full flex flex-col sm:flex-row sm:flex-wrap gap-8">
      <Goal :goalTitle="'A new bike'" :coverImage="'https://static.vecteezy.com/system/resources/thumbnails/044/600/540/small_2x/drawing-of-bike-handlebars-illustrated-cycling-safety-vector.jpg'"
        :currentAmount="245" :goalAmount="999"
      />
      <NewGoal />
    </span>
    
  </div>
</template>