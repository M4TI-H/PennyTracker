<script setup lang="ts">
import { ref } from "vue";
import type { NewGoal } from "@/types/savings";
import useSavings from "@/composables/useSavings";

const emit = defineEmits(["post-goal"]);

const { postNewGoal } = useSavings();
const displayForm = ref<boolean>(false);

const showForm = () => displayForm.value = true;
const hideForm = () => displayForm.value = false;

const newGoalData = ref<NewGoal>({
  title: "",
  amount: null,
  cover: "#000000",
  user_id: 2
});

const handlePostGoal = () => {
  postNewGoal(newGoalData.value);
  hideForm();
  emit("post-goal");
}

</script>

<template>
  <div @click="showForm" class="w-172 h-64 flex flex-col items-center justify-center 
  bg-[#E9ECEF]/70 hover:bg-[#E9ECEF]/100 rounded-xl shadow-xl border-2 border-neutral-800 border-dashed"
    :class="{'hover:cursor-pointer': !displayForm}">
     <p v-if="!displayForm" class="font-semibold text-4xl text-neutral-800">+</p>
     <span v-else class="relative w-full h-full flex flex-col items-center p-4 pb-2">
      <span class="flex w-full h-auto justify-between items-center">
        <div class="w-[5%]"></div>
        <p class="font-semibold text-lg text-neutral-800">Set new goal</p>
        <button @click.stop="hideForm"
        class="hover:cursor-pointer w-[5%]">
          <i class="pi pi-times text-xl"></i>
        </button>
      </span>
        
        <div class="h-[60%] w-full flex">
          <span class="flex flex-col items-center w-[60%] h-full">
            <input type="text" placeholder="Title of the goal" v-model="newGoalData.title"
              class="w-[70%] h-[30%] px-2 border-2 border-neutral-800 rounded-lg text-md 
              font-medium mt-4 outline-0"
            />
            <input type="number" placeholder="Goal amount" v-model="newGoalData.amount"
              class="w-[70%] h-[30%] px-2 border-2 border-neutral-800 rounded-lg text-md
              font-medium mt-4 outline-0"
            />
          </span>
          <span class="flex flex-col items-center justify-center w-[40%]">
            <span class="flex w-[70%] h-[50%] justify-between items-center">
              <label class="text-lg text-neutral-800 font-semibold">Select color</label> 
              <input type="color" v-model="newGoalData.cover"/>
            </span>
            <span class="flex w-[70%] h-[50%] justify-between items-center">
              <label class="text-lg text-neutral-800 font-semibold">Select icon</label> 
            </span>
          </span>
        </div>
       
        <button @click="handlePostGoal" class="w-[20%] h-10 rounded-3xl mt-auto bg-neutral-800 text-sm text-[#E9ECEF]
        border-neutral-800 border-2 hover:cursor-pointer hover:bg-[#588157]
          transition ease-in-out duration-200 mb-1"
        >Set</button>
     </span>
  </div>
</template>