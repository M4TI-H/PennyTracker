<script setup>
import { ref } from "vue";

const displayForm = ref(false);

const showForm = () => {
  displayForm.value = true;
}

const hideForm = () => {
  displayForm.value = false;
}

function formatDate(date) {
  return date.toISOString().split('T')[0];
}

const data = ref({
  title: undefined,
  amount: null,
  cover: undefined,
  user_id: 2
});

const postNewGoal = async() => {
  try {
    const response = await fetch("http://localhost:8000/savings/new_goal/", {
      method: "POST",
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        title: data.value.title, 
        goal_amount: parseFloat(data.value.amount), 
        current_amount: 0.0,
        cover: (data.value.cover === undefined) ? "https://insurance-blog-cms.paytminsurance.co.in/348_Top10_Savings_Plans_aac8eac493.jpg" : data.value.cover,
        finished: 0,
        creation_date: formatDate(new Date()),
        user_id: data.value.user_id
      })
    });

    if (!response.ok) {
      throw new Error (`HTTP error! Status: ${response.status}`);
    }

    data.value = {
      title: undefined,
      amount: null,
      cover: undefined,
      user_id: 2
    };

    hideForm();
  }
  catch (error) {
    console.error(`An error has occured while posting savings data: ${error}`);
  }
}

</script>

<template>
  <div @click="showForm" class="w-64 h-96 flex flex-col items-center justify-center opacity-70 hover:cursor-pointer
  bg-[#E9ECEF] rounded-xl shadow-xl border-2 border-neutral-800 border-dashed"
    :class="{'opacity-100': displayForm}">
     <p v-if="!displayForm" class="font-semibold text-4xl text-neutral-800">+</p>
     <span v-else class="w-full h-full flex flex-col items-center p-4 pb-2">
        <p class="font-semibold text-lg text-neutral-800">Set new goal</p>
        <input type="text" placeholder="Title of the goal" v-model="data.title"
          class="w-full h-10 px-2 border-2 border-neutral-800 rounded-lg text-md font-medium mt-4"
        />
        <input type="number" placeholder="Goal amount" v-model="data.amount"
          class="w-full h-10 px-2 border-2 border-neutral-800 rounded-lg text-md font-medium mt-4"
        />
        <input type="text" placeholder="Cover image link" v-model="data.cover"
          class="w-full h-10 px-2 border-2 border-neutral-800 rounded-lg text-md font-medium mt-4"
        />
        <p class="text-sm text-neutral-400 self-end mr-2">Optional</p>
        <button @click="postNewGoal" class="w-[70%] h-10 rounded-3xl mt-auto bg-neutral-800 text-sm text-[#E9ECEF]
        border-neutral-800 border-2 hover:cursor-pointer hover:bg-[#588157]
          transition ease-in-out duration-200 mb-1"
        >Set</button>
        <a @click.stop="hideForm" class="text-sm text-neutral-800 hover:underline">Cancel</a>
     </span>
  </div>
</template>