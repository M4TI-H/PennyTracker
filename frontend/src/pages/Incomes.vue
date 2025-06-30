<script setup>
import { ref, watchEffect } from "vue";
import Navigation from "@/components/navigation/Navigation.vue";
import CompactNavigation from "@/components/navigation/CompactNavigation.vue";

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
  </div>
</template>