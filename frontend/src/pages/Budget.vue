<script setup lang="ts">
import { ref, watch } from "vue";
import Navigation from "@/components/navigation/Navigation.vue";
import useScreenSize from "@/composables/useScreenSize";
import BudgetSection from "@/components/budget/BudgetSection.vue";
import BudgetDistribution from "@/components/budget/BudgetDistribution.vue";
import { refreshBudgetData } from "../stores/budgetData";

const {screenWidth, screenHeight} = useScreenSize();

const categoriesValues = ref<number[]>([]);
const categoriesShares = ref<number[]>([]);
const monthId = ref<string>("");

</script>

<template>
  <div class="fixed flex w-full h-full justify-around bg-[#DAD7CD] sm:py-16 ">
    <Navigation :screenWidth="screenWidth"/>
    <span class="w-[96rem] flex flex-row flex-wrap items-start gap-8">
      <BudgetSection :categoriesValues="categoriesValues" :categoriesShares="categoriesShares" v-model:month="monthId"/>
      <BudgetDistribution 
        v-model:categoriesValues="categoriesValues" 
        v-model:categoriesShares="categoriesShares" 
        :monthId="monthId"
        @refresh="refreshBudgetData.refreshNow(true)"/>
    </span>
  </div>
</template>