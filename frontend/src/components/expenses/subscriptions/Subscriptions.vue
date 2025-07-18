<script setup lang="ts">
import { onMounted, ref } from "vue";
import NewSubForm from "./NewSubForm.vue";
import type { Subscription } from "@/types/transactions";

const displayForm = ref<boolean>(false);

const switchFormDisplay = () => {
  displayForm.value = !displayForm.value;
}

const subscriptionsData = ref<Subscription[]>([]);

const fetchSubscriptions = async() => {
  try {
    const response = await fetch("http://localhost:8000/subscriptions/fetch_all");
    
    if (!response.ok) {
      throw new Error (`HTTP error! Status: ${response.status}`);
    }

    subscriptionsData.value = await response.json();
  }
  catch (error) {
    console.error(`An error has occured while fetching transactions data: ${error}`);
  }
}

onMounted(async () => {
  await fetchSubscriptions();
})

</script>

<template>
  <div class="relative sm:w-[39%] h-[38%] flex flex-col items-center bg-[#E9ECEF] p-4 rounded-xl shadow-xl">
    <span class="w-full flex justify-between self-end">
      <div class="w-[20%]"></div>
      <p class="text-2xl text-neutral-800 font-semibold mb-2">Subscriptions</p>
      <button @click="switchFormDisplay" class="w-[20%] rounded-3xl bg-none font-semibold text-sm text-neutral-800 
      border-neutral-800 border-2 hover:cursor-pointer hover:bg-neutral-800  hover:text-[#E9ECEF]
        transition ease-in-out duration-200">+ Add new</button>
    </span>
    <div class="w-[90%] h-8 flex items-center mb-1">
      <p class="w-[30%] text-md text-neutral-800 font-bold">Service</p>
      <p class="w-[20%] text-md text-neutral-800 font-bold">Amount</p>
      <p class="w-[20%] text-md text-neutral-800 font-bold">Frequency</p>
      <p class="w-[30%] text-md text-neutral-800 font-bold">Next payment</p>
    </div>
    <div class="w-[100%] flex flex-col items-center overflow-y-auto gap-2">
      <div v-for="sub in subscriptionsData" :key="sub.id" class="w-[90%] h-8 flex items-center">
        <p class="w-[30%] text-sm text-neutral-800 font-semibold">{{ sub.service }}</p>
        <p class="w-[20%] text-sm text-neutral-800 font-semibold">{{ sub.amount }}</p>
        <p class="w-[20%] text-sm text-neutral-800 font-semibold">{{ sub.frequency }}</p>
        <p class="w-[30%] text-sm text-neutral-800 font-semibold">{{ sub.start_date }}</p>
      </div>
    </div>
    
   <NewSubForm :displayForm="displayForm" @close="switchFormDisplay" @submit="fetchSubscriptions"/>
</div>
</template>