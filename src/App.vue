<script setup>
import Navigation from "@/components/Navigation.vue";
import NameCard from "@/components/NameCard.vue";
import AccountState from "@/components/AccountState.vue";
</script>

<template>
  <div class="w-screen h-screen bg-[#DAD7CD] flex px-8 gap-16">
    <!--Menu bar with buttons-->
    <Navigation />
    <!--User welcome card-->
    <div class="h-auto w-auto flex flex-col gap-4">
      <NameCard />
      <div class="flex gap-8">
        <AccountState :account="'PayPal'" :balance="'215.78'"/>
        <AccountState :account="'mBank'" :balance="'1451.83'"/>
      </div>
    </div>
  </div>
</template>