<script setup>
import { ref } from "vue";

const displayForm = ref(false);

const showForm = () => {
  displayForm.value = true;
}

const hideForm = () => {
  displayForm.value = false;
}

</script>

<template>
  <div @click="showForm" class="w-64 h-96 flex flex-col items-center justify-center opacity-70 hover:cursor-pointer
  bg-[#E9ECEF] rounded-xl shadow-xl border-2 border-neutral-800 border-dashed"
    :class="{'opacity-100': displayForm}">
     <p v-if="!displayForm" class="font-semibold text-4xl text-neutral-800">+</p>
     <span v-else class="w-full h-full flex flex-col items-center p-4 pb-2">
        <p class="font-semibold text-lg text-neutral-800">Set new goal</p>
        <input type="text" placeholder="Name of goal" class="w-full h-10 px-2 border-2 border-neutral-800 rounded-lg text-md font-medium mt-4"/>
        <input type="number" placeholder="Goal amount" class="w-full h-10 px-2 border-2 border-neutral-800 rounded-lg text-md font-medium mt-4"/>
        <input type="file" class="w-full h-[30%] border-2 border-neutral-800 rounded-lg text-md font-medium mt-4"/>
        <button class="w-[50%] h-8 rounded-3xl mt-auto bg-neutral-800 text-sm text-[#E9ECEF]
        border-neutral-800 border-2 hover:cursor-pointer hover:bg-[#588157]
          transition ease-in-out duration-200 mb-1"
        >Set</button>
        <a @click.stop="hideForm" class="text-sm text-neutral-800 hover:underline">Cancel</a>
     </span>
  </div>
</template>