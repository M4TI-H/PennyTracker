<script setup lang="ts">
import { ref } from "vue";
import type { NewSubscription } from "@/types/transactions";
import useSubscriptions from "@/composables/useSubscriptions";

const { displayForm} = defineProps<{
  displayForm: boolean,
}>();

const emit = defineEmits<{
  (e: "close"): void
  (e: "submit"): void
}>();

const { postNewSubscription } = useSubscriptions();

const newSubData = ref<NewSubscription>({
  service: "",
  amount: 0,
  start_date: "",
  frequency: "",
});

const closeForm = () => {
  newSubData.value = {
    service: "",
    amount: 0,
    start_date: "",
    frequency: ""
  }

  emit("close");
}

const frequencies = ["Daily", "Weekly", "Monthly", "Yearly"];

const handlePostSub = async () => {
  await postNewSubscription(newSubData.value, 2);
  emit("close");
  emit("submit");
}

</script>

<template>
  <div v-if="displayForm" @click="closeForm"
    class="absolute w-full h-full bg-neutral-800/80 top-0 rounded-xl flex justify-center items-center"
  >
    <div @click.stop class="absolute w-[50%] h-[90%] bg-[#E9ECEF] rounded-xl p-2 flex flex-col items-center gap-1">
      <p class="text-xl text-neutral-800 font-semibold">New subscription</p>
      <button @click="closeForm"class="absolute right-4 top-3 hover:cursor-pointer">
        <i class="pi pi-times"></i>
      </button>
      <input type="text" placeholder="Name of service" v-model="newSubData.service"
        class="w-[90%] h-10 bg-[#FFF] border-2 border-neutral-800 rounded-lg font-semibold text-md px-2 focus:outline-0"
      />
      <input type="number" placeholder="Amount" v-model="newSubData.amount"
        class="w-[90%] h-10 bg-[#FFF] border-2 border-neutral-800 rounded-lg font-semibold text-md px-2 focus:outline-0"
      />
      <span class="w-[90%] flex items-center justify-between gap-4">
        <p class="text-md text-neutral-800 font-semibold">Start date:</p>
        <input type="date" v-model="newSubData.start_date"
          class="h-10 bg-[#FFF] border-2 border-neutral-800 rounded-lg font-semibold text-md px-2 focus:outline-0"
        />
      </span>
      <span class="w-[90%] flex items-center justify-between gap-4">
        <p class="text-md text-neutral-800 font-semibold">Frequency:</p>
        <select v-model="newSubData.frequency"
          class="w-35 h-10 bg-[#FFF] border-2 border-neutral-800 rounded-lg font-semibold text-md px-2 focus:outline-0"
        >
          <option v-for="frequency in frequencies" :value="frequency" :key="frequency">{{ frequency }}</option> 
        </select>
      </span>
      <button @click="handlePostSub"
      class="w-32 h-10 rounded-3xl bg-neutral-800 text-sm text-[#E9ECEF]
        border-neutral-800 border-2 hover:cursor-pointer hover:bg-[#588157]
        transition ease-in-out duration-200"
      >Confirm</button>
    </div>
  </div>
</template>