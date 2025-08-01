<script setup lang="ts">
import { onMounted, ref, watchEffect } from "vue";
import AccountView from "./AccountView.vue";
import useAccounts from "@/composables/useAccounts";
import type { Account } from "@/types/options";
const displayNewAccount = ref(false);
const displayDeleteAccount = ref(false);

const { accountsData, fetchAccounts, postNewAccount } = useAccounts();

const refreshAccounts = () => {
  fetchAccounts(2);
}

const newAccountName = ref<string>("");

const handleNewAccount = (user: number) => {
  postNewAccount(user, newAccountName.value);
  switchDisplayNewAccount();
}

onMounted(async () => {
  refreshAccounts();
})

const switchDisplayNewAccount = () => {
  displayNewAccount.value = !displayNewAccount.value;
  displayDeleteAccount.value = false;
}

</script>

<template>
  <div class="w-[60%] h-[40%] flex flex-wrap gap-4">
    <AccountView v-for="account in accountsData" :key="account.id" :account="account" @delete="refreshAccounts()"/>

    <div @click="switchDisplayNewAccount"
      class="w-64 h-32 flex flex-col p-4
      items-center justify-center
      rounded-xl shadow-xl bg-[#E9ECEF]/70
      border-2 border-dashed
      hover:scale-101 hover:cursor-pointer hover:bg-[#E9ECEF]/100
      transition ease-in-out duration-200"
      :class="{'hidden': displayNewAccount}"
    >
       <p class="font-semibold text-4xl text-neutral-800" >+</p>
    </div>
    
    <!--New account form-->
    <div
      class="w-64 h-32 flex flex-col p-4
      items-center gap-2
      rounded-xl shadow-xl bg-[#E9ECEF]/70
      border-2 border-dashed"
      :class="{'hidden': !displayNewAccount}" 
    >
      <input type="text" placeholder="Account name" v-model="newAccountName"
        class="w-full h-10 bg-[#FFF] border-2 border-neutral-800 rounded-lg font-semibold text-md px-2 focus:outline-0"
      />
      <span class="h-10 w-full flex justify-between mt-auto">
        <button @click="switchDisplayNewAccount" 
          class="w-[45%] h-full rounded-3xl bg-none text-sm text-neutral-800
          border-neutral-800 border-2 hover:cursor-pointer transition ease-in-out duration-200"
        >Cancel</button>
        <button @click="handleNewAccount(2)"
          class="w-[45%] h-full rounded-3xl bg-neutral-800 text-sm text-[#E9ECEF]
          border-neutral-800 border-2 hover:cursor-pointer transition ease-in-out duration-200"
        >Confirm</button>
      </span>
    </div>
  </div>
</template>