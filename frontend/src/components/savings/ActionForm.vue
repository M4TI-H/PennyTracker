<script setup>
import { computed, ref } from 'vue';
import formatDate from '@/composables/formatDate';

const props = defineProps({
  showWithdraw: Boolean,
  showDeposit: Boolean,
  goal: Object
});

const emit = defineEmits(["close", "post-action"]);

const amount = ref(null);
const action = computed(() => {
  if (props.showDeposit) return 'deposit';
  else if (props.showWithdraw) return 'withdraw';
  else return null;
});

const postNewGoalAction = async() => {
  const inputAmount = parseFloat(amount.value);
  try {
    const response = await fetch("http://localhost:8000/savings/new_goal_action/", {
      method: "POST",
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        type: action.value, 
        amount: inputAmount, 
        date: formatDate(new Date()),
        goal_id: props.goal.id,
        user_id: props.goal.user_id
      })
    });

    if (!response.ok) {
      const err = await response.json()
      throw new Error(err.detail);
    }

    const result = await response.json();

    if (result.status === "success"){
      emit("post-action", { amount: inputAmount, action: action.value });
      amount.value = null;
    }
    else {
      console.error(`Backend error: ${result.detail}`)
    }
  }
  catch (error) {
    console.error(`An error has occured while posting savings actions data: ${error}`);
  }
}

function onClose() {
  amount.value = null;
  emit('close');
}

</script>

<template>
    <div v-if="showDeposit || showWithdraw" class="w-[40%] h-full flex flex-col justify-center items-center">
      <span class="flex w-full h-[40%]">
        <input type="number" v-model="amount"
          :placeholder="showWithdraw ? 'Withdraw amount' : (showDeposit ? 'Deposit amount' : '')"
          class="w-[80%] h-full px-2 border-2 border-neutral-800 rounded-l-lg border-r-0 text-md font-medium focus:outline-0"
        />
        <button @click="postNewGoalAction"
          class="w-[20%] h-full rounded-r-lg bg-none font-semibold text-sm text-neutral-800 
        border-neutral-800 border-2 hover:cursor-pointer hover:text-[#E9ECEF]
          transition ease-in-out duration-200" 
          :class="showWithdraw ? 'hover:bg-[#BC4749]': 'hover:bg-[#588157]'"
        ><i class="pi pi-check text-xl"></i></button>
      </span>
      
      <a v-if="showDeposit || showWithdraw" @click="onClose"
        class="text-sm text-neutral-800 hover:underline hover:cursor-pointer mt-2"
      >Cancel</a>
    </div>
</template>