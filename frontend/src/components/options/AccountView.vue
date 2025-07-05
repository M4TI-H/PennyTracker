<script setup>
import { ref } from "vue";

const props = defineProps({
  account: Object
});

const displayDeposit = ref(false);
const deposit = ref(null);

const deleteAccount = async (account_id, user_id) => {
  try {
    const url = new URL("http://localhost:8000/transactions/delete_account/");
    url.searchParams.append("account_id", account_id);
    url.searchParams.append("user_id", user_id);

    const response = await fetch(url.toString(), {
      method: "DELETE"
    });

    if (!response.ok) {
      throw new Error (`HTTP error! Status: ${response.status}`);
    }

    fetchAccounts(2);
    switchDisplayDeleteAccount();
  }
  catch (error) {
     console.error(`An error has occured while deleting an account: ${error}`);
  }
}

const switchDisplayDeposit = () => {
  displayDeposit.value = !displayDeposit.value;
  deposit.value = null;
}
</script>

<template>
  <div class="w-64 flex flex-col p-4 justify-between
    rounded-xl shadow-xl bg-[#E9ECEF]"
    :class="{'h-40': displayDeposit, 'h-32': !displayDeposit}"
  >
    <span class="w-full flex justify-between items-center">
      <p class="text-md sm:text-xl text-[#212529] font-semibold">{{ account.name }}</p>
      <div>
        <button @click="switchDisplayDeposit"
          class="text-xl hover:scale-110 hover:cursor-pointer transition ease-in-out duration-200 mr-4"
        ><i class="pi pi-plus"></i></button>
        <button @click="deleteAccount(account.id, 2)"
          class="text-xl hover:scale-110 hover:cursor-pointer transition ease-in-out duration-200"
        ><i class="pi pi-trash"></i></button>
      </div>
    </span>
    <span v-if="displayDeposit" class="flex h-10">
      <input type="number" v-model="deposit"
        placeholder="Deposit amount"
        class="w-[80%] h-full px-2 border-2 border-neutral-800 rounded-l-lg border-r-0 text-md font-medium focus:outline-0"
      />
      <button @click="switchDisplayDeposit"
        class="w-[20%] h-full rounded-r-lg bg-none font-semibold text-sm bg-neutral-800
      border-neutral-800 border-2 hover:cursor-pointer text-[#E9ECEF] 
        transition ease-in-out duration-200" 
      ><i class="pi pi-check text-xl"></i></button>
    </span>
    <span class="flex items-end justify-end h-10">
      <p class="text-2xl sm:text-4xl text-[#212529] font-bold mt-4">
        ${{ parseFloat(account.balance).toFixed(2).split('.')[0] }}
      </p>
      <p class="text-md sm:text-xl text-[#212529] font-semibold mt-4">
        .{{ parseFloat(account.balance).toFixed(2).split('.')[1] }}
      </p>
    </span>
  </div>
</template>