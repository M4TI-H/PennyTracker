<script setup>
import { ref } from "vue";

defineProps({
  goalTitle: String,
  coverImage: String,
  goalAmount: Number,
  currentAmount: Number
});

const displayButtons = ref(true);
const showDeposit = ref(false);
const showWithdraw = ref(false);

const hideInput = () => {
  showDeposit.value = false;
  showWithdraw.value = false;
  displayButtons.value = true;
}

const displayDepositInput = () => {
  showDeposit.value = true;
  displayButtons.value = false;
}

const displayWithdrawInput = () => {
  showDeposit.value = true;
  displayButtons.value = false;
}

</script>

<template>
  <div class="w-64 h-96 flex flex-col items-center p-4
  bg-[#E9ECEF] rounded-xl shadow-xl">
    <img :src="coverImage"
      class="w-[100%] h-[30%] rounded-lg mb-2"/>
    <p class="text-lg font-bold text-neutral-800">{{ goalTitle }}</p>
    <p class="text-md font-semibold text-neutral-800">${{ currentAmount }} / ${{ goalAmount }}</p>
    <hr class="bg-neutral-300 w-[96%] h-[2px] border-0 mt-2"/>
    <p class="text-sm font-bold text-neutral-400">Recent transactions</p>
    <span class="w-[80%] flex justify-between">
      <p class="text-sm font-bold text-neutral-400">22.06.25</p>
      <p class="text-sm font-bold text-neutral-400">+$100</p>
    </span>
    <hr class="bg-neutral-300 w-[96%] h-[2px] border-0 mt-auto"/>
    <span v-if="displayButtons" class="w-[100%] h-[10%] flex justify-between mt-auto">
      <button @click="displayDepositInput" class="w-[48%] rounded-3xl bg-neutral-800 text-sm text-[#E9ECEF]
      border-neutral-800 border-2 hover:cursor-pointer hover:bg-[#588157]
        transition ease-in-out duration-200">Add funds</button>
      <button @click="displayWithdrawInput" class="w-[48%] rounded-3xl bg-none font-semibold text-sm text-neutral-800 
       border-neutral-800 border-2 hover:cursor-pointer hover:bg-[#BC4749] hover:text-[#E9ECEF]
        transition ease-in-out duration-200">Withdraw</button>
    </span>

    <span v-if="showDeposit" class="w-[100%] h-[10%] flex items-center justify-between mt-auto">
      <input type="number" placeholder="Deposit value" class="w-[70%] h-full px-2 border-2 border-neutral-800 rounded-l-lg border-r-0 text-md font-medium focus:outline-0"/>
      <button @click="hideInput" class="w-[30%] h-full rounded-r-lg bg-none font-semibold text-sm text-neutral-800 
      border-neutral-800 border-2 hover:cursor-pointer hover:bg-[#588157] hover:text-[#E9ECEF]
        transition ease-in-out duration-200">Confirm</button>
    </span>

    <span v-if="showWithdraw" class="w-[100%] h-[10%] flex items-center justify-between mt-auto">
      <input type="number" placeholder="Withdrawal value" class="w-[70%] h-full px-2 border-2 border-neutral-800 rounded-l-lg border-r-0 text-md font-medium focus:outline-0"/>
      <button @click="hideInput" class="w-[30%] h-full rounded-r-lg bg-none font-semibold text-sm text-neutral-800 
      border-neutral-800 border-2 hover:cursor-pointer hover:bg-[#588157] hover:text-[#E9ECEF]
        transition ease-in-out duration-200">Confirm</button>
    </span>

     <a v-if="showDeposit || showWithdraw" 
      @click="hideInput"
      class="text-sm text-neutral-800 hover:underline hover:cursor-pointer mt-2"
    >Cancel</a>
  </div>
</template>