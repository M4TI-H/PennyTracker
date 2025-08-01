<script setup lang="ts">
import { onMounted, ref } from "vue";
import NewSubForm from "./NewSubForm.vue";
import useSubscriptions from "@/composables/useSubscriptions";

const displayForm = ref<boolean>(false);

const { subscriptionsData, fetchSubscriptions, deleteSubscription, calculateNextPayment } = useSubscriptions();

const handleDelete = async (sub_id: number) => {
  await deleteSubscription(2, sub_id)
  await fetchSubscriptions(2);
}

const switchFormDisplay = () => {
  displayForm.value = !displayForm.value;
}

onMounted(() => fetchSubscriptions(2));

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
      <p class="w-[25%] text-md text-neutral-800 font-bold">Service</p>
      <p class="w-[20%] text-md text-neutral-800 font-bold">Amount</p>
      <p class="w-[20%] text-md text-neutral-800 font-bold">Frequency</p>
      <p class="w-[25%] text-md text-neutral-800 font-bold">Next payment</p>
      <p class="w-[10%] text-md text-neutral-800 font-bold">Action</p>
    </div>
    <div class="w-[100%] flex flex-col items-center overflow-y-auto gap-2">
      <div v-for="sub in subscriptionsData" :key="sub.id" class="w-[90%] h-8 flex items-center">
        <p class="w-[25%] text-sm text-neutral-800 font-semibold">{{ sub.service }}</p>
        <p class="w-[20%] text-sm text-neutral-800 font-semibold">{{ sub.amount }}</p>
        <p class="w-[20%] text-sm text-neutral-800 font-semibold">{{ sub.frequency }}</p>
        <p class="w-[25%] text-sm text-neutral-800 font-semibold">{{ calculateNextPayment(sub.start_date, sub.frequency).slice(0, 10) }}</p>
        <button @click="handleDelete(sub.id)" class="w-[10%] hover:cursor-pointer transition ease-in-out duration-200 hover:scale-120"><i class="pi pi-trash"></i></button>
      </div>
    </div>
    
   <NewSubForm :displayForm="displayForm" @close="switchFormDisplay" @submit="fetchSubscriptions(2)"/>
</div>
</template>