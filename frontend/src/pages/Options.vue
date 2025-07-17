<script setup lang="ts">
import Navigation from "@/components/navigation/Navigation.vue";
import CompactNavigation from "@/components/navigation/CompactNavigation.vue";
import ManageCategories from "@/components/options/ManageCategories.vue";
import ManageAccounts from "@/components/options/ManageAccounts.vue";
import useScreenSize from "@/composables/screenSize.ts";

const smallW = 640;

const {screenWidth, screenHeight} = useScreenSize();

</script>
<template>
  <div class="fixed flex w-full h-full justify-center gap-16 bg-[#DAD7CD] sm:py-16 ">
    <!--Menu bar with buttons-->
    <Navigation v-if="screenWidth >= smallW" :screenWidth="screenWidth"/>
    <CompactNavigation v-else/>
      <span class="max-w-[96rem] h-auto w-full flex flex-wrap sm:flex-row sm:flex-wrap gap-8 overflow-y-auto">
        <ManageCategories />
        <ManageAccounts />
      </span>
  </div>
</template>