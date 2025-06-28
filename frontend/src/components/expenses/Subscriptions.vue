<script setup>
import { ref } from "vue";
defineProps({
  subsriptions: Array,
});

const displayForm = ref(false);

const switchFormDisplay = () => {
  displayForm.value = !displayForm.value;
}

</script>

<template>
  <div class="relative sm:w-[39%] h-[38%] flex flex-col items-center bg-[#E9ECEF] p-4 rounded-xl shadow-xl">
    <span class="w-full flex justify-between self-end">
      <div class="w-[20%]"></div>
      <p class="text-2xl text-neutral-800 font-semibold mb-2">Subscriptions</p>
      <button @click="switchFormDisplay" class="w-[20%] rounded-3xl bg-none font-semibold text-sm text-neutral-800 
      border-neutral-800 border-2 hover:cursor-pointer hover:bg-[#588157] hover:text-[#E9ECEF]
        transition ease-in-out duration-200">+ Add new</button>
    </span>
    <div class="w-[90%] h-8 flex items-center">
    <p class="w-[40%] text-md text-neutral-800 font-bold">Service</p>
    <p class="w-[30%] text-md text-neutral-800 font-bold">Amount</p>
    <p class="w-[30%] text-md text-neutral-800 font-bold">Next payment</p>
    </div>
    <div v-for="sub in subsriptions" :key="sub.id" class="w-[90%] h-8 flex items-center">
    <p class="w-[40%] text-sm text-neutral-800 font-semibold">{{ sub.service }}</p>
    <p class="w-[30%] text-sm text-neutral-800 font-semibold">{{ sub.amount }}</p>
    <p class="w-[30%] text-sm text-neutral-800 font-semibold">{{ sub.next_payment }}</p>
    </div>
    <div v-if="displayForm" class="absolute w-full h-full bg-neutral-800/80 top-0 rounded-xl flex justify-center items-center">
      <div class="absolute w-[50%] h-[90%] bg-[#E9ECEF] rounded-xl p-4 flex flex-col items-center">
        <p class="text-xl text-neutral-800 font-semibold">New subscription</p>
        <input type="text" placeholder="Name of service"/>
        <input type="number" placeholder="Amount"/>
        <span class="flex">
          <p>Next payment</p>
          <input type="date"/>
        </span>
        <span class="flex">
          <p>Frequency</p>
          <select>
            <option>Daily</option>
            <option>Weekly</option>
            <option>Monthly</option>
            <option>Annually</option>
          </select>
        </span>
        <a @click="switchFormDisplay" 
          class="text-sm text-neutral-800 hover:underline hover:cursor-pointer mt-2"
        >Cancel</a>
      </div>
    </div>
</div>
</template>