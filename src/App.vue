<script setup>
import Navigation from "@/components/Navigation.vue";
import NameCard from "@/components/dashboard/NameCard.vue";
import AccountState from "@/components/dashboard/AccountState.vue";
import PiggyBank from "./components/dashboard/PiggyBank.vue";
import ExpensesSummary from "./components/dashboard/ExpensesSummary.vue";
import { ref, watchEffect } from "vue";
import CompactNavigation from "./components/CompactNavigation.vue";

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
  <div class="fixed w-full h-full bg-[#DAD7CD] sm:py-16">
    <!--Menu bar with buttons-->
    <Navigation v-if="screenWidth >= smallW" :screenWidth="screenWidth" />
    <CompactNavigation v-else/>
    <!--Cards grid-->
    <span class="flex flex-col sm:flex-wrap items-center sm:items-start sm:justify-center w-[100%] h-[100%] sm:max-w-392 gap-2 py-2 sm:mt-0">
      <div class="min-h-1/5 sm:h-104 sm:min-w-96 w-[90%] sm:w-[30%] flex flex-col gap-2">
        <!--User welcome card-->  
        <NameCard />
        <span class="flex gap-2">
          <AccountState :account="'PayPal'" :balance="'215.78'"/>
          <AccountState :account="'mBank'" :balance="'1451.83'"/>
        </span>
      </div>
      <ExpensesSummary :screenWidth="screenWidth"/>
      <span class="flex w-[90%] gap-2">
        <div class="max-w-[50%] sm:min-w-128 sm:max-w-[60%] w-full h-32 sm:h-96 bg-[#E9ECEF] p-4 rounded-xl shadow-xl">
          <p>Some chart here</p>
        </div>
        <PiggyBank :screenWidth="screenWidth"/>
      </span>
      
    </span>
  </div>
</template>