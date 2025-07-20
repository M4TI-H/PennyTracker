<script setup lang="ts">
import { ref, watchEffect, onMounted } from "vue";
import Navigation from "@/components/navigation/Navigation.vue";
import CompactNavigation from "@/components/navigation/CompactNavigation.vue";
import NameCard from "@/components/dashboard/NameCard.vue";
import PiggyBank from "@/components/dashboard/PiggyBank.vue";
import ExpensesSummary from "@/components/dashboard/ExpensesSummary.vue";
import AccountView from "@/components/options/AccountView.vue";
import { fetchTopAccounts } from "@/composables/fetchAccounts.ts";
import useScreenSize from "@/composables/screenSize.ts";
import TransactionCount from "@/components/dashboard/TransactionCount.vue";
import type { Account } from "@/types/options";

const smallW = 640;
const {screenWidth, screenHeight} = useScreenSize();

const accountsData = ref<Account[]>([]);

const refreshAccounts = async () => {
  accountsData.value = await fetchTopAccounts(2);
}

onMounted(async() => {
  refreshAccounts();
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
          <AccountView v-for="account in accountsData" :key="account.id" :account="account" @delete="refreshAccounts()"/>
        </span>
      </div>
      <ExpensesSummary />
      <span class="flex w-[90%] max-h-[15%] sm:max-h-[50%] h-full gap-4">
        <TransactionCount />
        <PiggyBank />
      </span>
    </span>
  </div>
</template>