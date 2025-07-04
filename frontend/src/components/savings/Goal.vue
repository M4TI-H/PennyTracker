<script setup>
import { onUpdated, ref, watch } from "vue";
import ActionForm from "./ActionForm.vue";

const { goal } = defineProps({
  goal: Object
});

const emit = defineEmits(["refresh"]);

const displayButtons = ref(true);
const showDeposit = ref(false);
const showWithdraw = ref(false);

const goalPercentage = ref("0%");

const actionsData = ref([]);

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
  showWithdraw.value = true;
  displayButtons.value = false;
}

const depositFunds = async(goal, amount, type) => {
  try {
    const url = new URL(`http://localhost:8000/savings/${type}/`);
    url.searchParams.append("user_id", goal.user_id);
    url.searchParams.append("goal_id", goal.id);
    url.searchParams.append("amount", amount);
    
    const response = await fetch(url.toString(), {
      method: "PUT"
    });

    if (!response.ok) {
      const err = await response.json()
      throw new Error(err.detail);
    }

    const result = await response.json();

    if (result.status === "success"){
      emit("refresh");
    }
    else {
      console.error(`Backend error: ${result.detail}`)
    }
  }
  catch (error) {
    console.error(`An error has occured while fetching savings actions data: ${error}`);
  }
}

const fetchSavingActions = async(goal_id, user_id) => {
  try {
    const url = new URL("http://localhost:8000/savings/fetch_actions/");
    url.searchParams.append("user_id", user_id);
    url.searchParams.append("goal_id", goal_id);
    
    const response = await fetch(url.toString());

    if (!response.ok) {
      throw new Error (`HTTP error! Status: ${response.status}`);
    }

    actionsData.value = await response.json();
  }
  catch (error) {
    console.error(`An error has occured while fetching savings actions data: ${error}`);
  }
}

const deleteGoal = async(user_id, transaction) => {
  try {
    const url = new URL("http://localhost:8000/savings/delete_goal/");
    url.searchParams.append("user_id", user_id);
    url.searchParams.append("goal_id", transaction);

    const response = await fetch(url.toString(), {
      method: "DELETE"
    });

    if (!response.ok) {
      throw new Error (`HTTP error! Status: ${response.status}`);
    }

    emit("refresh");
  }
  catch (error) {
     console.error(`An error has occured while deleting a saving goal: ${error}`);
  }
}

const handleActionPost = (amount, action) => {
  fetchSavingActions(goal.id, 2);
  depositFunds(goal, amount, action);
  hideInput();
}



onUpdated(() => {
  const percentage = (goal.current_amount / goal.goal_amount) * 100;
  goalPercentage.value = `${percentage}%`;
});

watch(() => goal?.id, (newGoalId) => {
  if (newGoalId) {
    fetchSavingActions(goal.id, 2)
  }
},{ immediate: true });

</script>

<template>
  <div class="relative w-172 h-64 flex flex-col items-start p-4 bg-[#E9ECEF] rounded-xl shadow-xl">
    <button @click="deleteGoal(goal.user_id, goal.id)"
      class="absolute right-5 top-4 hover:cursor-pointer transition ease-in-out duration-200 hover:scale-120"
    >
      <i class="pi pi-trash"></i>
    </button>
    <div class="flex w-full h-[20%]">
      <i class="pi pi-star-fill w-[10%] text-4xl text-center" :style="{ color: goal.cover }"></i>
      <span class="flex justify-between w-[90%] h-full">
        <p class="text-2xl font-bold mt-1" :style="{ color: goal.cover }">{{ goal.title }}</p>
        
      </span>
    </div>
    
    <div class="w-full h-[50%] flex">
      <div class="w-[60%] h-full border-t-2 flex flex-col items-center border-neutral-400">
        <p class="text-xs h-1/6 text-neutral-400 font-semibold">Recent actions</p>
        <span v-for="action in actionsData" :key="action.id" class="w-[90%] h-1/6 flex justify-between">
          <p class="text-xs text-neutral-400 font-semibold">{{ action.date }}</p>
          <p class="text-xs text-neutral-400 font-semibold">{{ action.type === 'deposit' ? "+" : "-" }}${{ action.amount }}</p>
        </span>
      </div>
      <div v-if="displayButtons" class="w-[40%] h-full flex flex-col justify-evenly items-center">
        <button @click="displayDepositInput" class="w-[40%] h-[30%] rounded-3xl bg-neutral-800 text-sm text-[#E9ECEF]
        border-neutral-800 border-2 hover:cursor-pointer hover:bg-[#588157]
          transition ease-in-out duration-200">Add funds</button>
        
        <button @click="displayWithdrawInput" class="w-[40%] h-[30%] rounded-3xl bg-none font-semibold text-sm text-neutral-800 
        border-neutral-800 border-2 hover:cursor-pointer hover:bg-[#BC4749] hover:text-[#E9ECEF]
          transition ease-in-out duration-200">Withdraw</button>
      </div>
      <ActionForm :showDeposit="showDeposit" :showWithdraw="showWithdraw" :goal="goal"
      @close="hideInput" @post-action="({amount, action}) => handleActionPost(amount, action)"/>
    </div>
    <div class="w-full h-[30%] flex flex-col gap-1">
      <p class="text-2xl font-semibold text-neutral-800 self-end" :class="{'line-through': goal.finished === 1}">${{ goal.current_amount }} / ${{ goal.goal_amount }}</p>
      <div class="w-full h-3 rounded-md bg-neutral-400">
        <div class="h-3 rounded-md" :style="{backgroundColor: goal.cover, width: goalPercentage }"></div>
      </div>
    </div>
    <p class="absolute left-5 bottom-2 text-sm text-neutral-400 font-semibold">{{ goal.creation_date }}</p>
  </div>
</template>