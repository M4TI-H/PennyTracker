<script setup>
  import { ref, watchEffect } from "vue";
  import Navigation from "@/components/navigation/Navigation.vue";
  import CompactNavigation from "@/components/navigation/CompactNavigation.vue";
  import NameCard from "@/components/dashboard/NameCard.vue";
  import AccountState from "@/components/dashboard/AccountState.vue";
  import PiggyBank from "@/components/dashboard/PiggyBank.vue";
  import ExpensesSummary from "@/components/dashboard/ExpensesSummary.vue";

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
  <div class="fixed flex w-full h-full justify-around bg-[#DAD7CD] sm:py-16 ">
    <!--Menu bar with buttons-->
    <Navigation v-if="screenWidth >= smallW" :screenWidth="screenWidth"/>
    <CompactNavigation v-else/>
    <!--Cards grid-->
    <span class="max-w-[96rem] p-2 sm:p-0 flex flex-col sm:flex-row sm:flex-wrap items-center sm:items-start gap-4">
      <div class="sm:min-w-96 sm:max-w-[40%] sm:w-[30%] min-h-[30%] max-h-[10%] w-full flex flex-col gap-4">
        <!--User welcome card-->  
        <NameCard />
        <span class="flex h-[55%] sm:h-32 gap-2">
          <AccountState :account="'PayPal'" :balance="'215.78'"/>
          <AccountState :account="'mBank'" :balance="'1451.83'"/>
        </span>
      </div>
      <ExpensesSummary :screenWidth="screenWidth"/>
      <span class="flex w-[90%] max-h-[15%] sm:max-h-[50%] h-full gap-4">
        <div class="max-w-[50%] sm:max-w-[60%] w-full sm:min-w-128 sm:h-96 bg-[#E9ECEF] p-4 rounded-xl shadow-xl">
          <p>Some chart here</p>
        </div>
        <PiggyBank :screenWidth="screenWidth"/>
      </span>
      
    </span>
  </div>
</template>