<script setup>
import { ref, watchEffect } from "vue";
import AccountView from "./AccountView.vue";
const displayNewAccount = ref(false);
const displayDeleteAccount = ref(false);

const newAccount = ref({
  name: undefined, 
  balance: 0,
  allow_negative: 1
});

const accountsData = ref([]);

const fetchAccounts = async(user) => {
  try {
    const url = new URL("http://localhost:8000/transactions/fetch_accounts");
    url.searchParams.append("user_id", user);
    
    const response = await fetch(url.toString());

    if (!response.ok) {
      throw new Error (`HTTP error! Status: ${response.status}`);
    }
    accountsData.value = await response.json();
  }
  catch (error) {
    console.error(`An error has occured while fetching accounts data: ${error}`);
  }
}

const postNewAccount = async (user_id) => {
  console.log(user_id, newAccount.value);
  try {
    const response = await fetch("http://localhost:8000/transactions/new_account/", {
      method: "POST",
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        name: newAccount.value.name,
        balance: newAccount.value.balance,
        allow_negative: newAccount.value.allow_negative,
        user_id: user_id
      })
    });

    if (!response.ok) {
      const err = await response.json()
      throw new Error(err.detail); 
    }

    fetchAccounts(2);
    switchDisplayNewAccount();
  }
  catch (error) {
    console.error(`An error has occured while posting new account: ${error}`);
  }
}


watchEffect(() => fetchAccounts(2));

const switchDisplayNewAccount = () => {
  displayNewAccount.value = !displayNewAccount.value;
  displayDeleteAccount.value = false;
  newAccount.value = {
    name: undefined, 
    balance: 0,
    allow_negative: 1
  };
}
const switchDisplayDeleteAccount = () => {
  displayDeleteAccount.value = !displayDeleteAccount.value;
  displayNewAccount.value = false;
}


</script>

<template>
  <div class="w-[60%] h-[40%] flex flex-wrap gap-4">
    <AccountView v-for="account in accountsData" :key="account.id" :account="account"/>

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
      class="w-64 h-64 flex flex-col p-4
      items-center gap-4
      rounded-xl shadow-xl bg-[#E9ECEF]/70
      border-2 border-dashed"
      :class="{'hidden': !displayNewAccount}" 
    >
      <p class="text-xl text-neutral-800 font-semibold">New account</p>
      <input type="text" placeholder="Account name" v-model="newAccount.name"
        class="w-full h-10 bg-[#FFF] border-2 border-neutral-800 rounded-lg font-semibold text-md px-2 focus:outline-0"
      />
      <input type="number" placeholder="Account balance" v-model="newAccount.balance"
        class="w-full h-10 bg-[#FFF] border-2 border-neutral-800 rounded-lg font-semibold text-md px-2 focus:outline-0"
      />
      <span class="h-10 w-full flex justify-end items-center mt-auto gap-4">
        <label class="text-sm text-neutral-800 font-semibold">Allow negative balance</label>
        <input type="checkbox" v-model="newAccount.allow_negative"/>
      </span>
      <span class="h-10 w-full flex justify-between mt-auto">
        <button @click="switchDisplayNewAccount" 
          class="w-[40%] h-full rounded-3xl bg-none text-sm text-neutral-800
          border-neutral-800 border-2 hover:cursor-pointer transition ease-in-out duration-200"
        >Cancel</button>
        <button @click="postNewAccount(2)"
          class="w-[40%] h-full rounded-3xl bg-neutral-800 text-sm text-[#E9ECEF]
          border-neutral-800 border-2 hover:cursor-pointer transition ease-in-out duration-200"
        >Confirm</button>
      </span>
    </div>
  </div>
</template>