<script setup>
import { ref, watch } from "vue";

const { goal } = defineProps({
  goal: Object
});

const displayButtons = ref(true);
const showDeposit = ref(false);
const showWithdraw = ref(false);

const amount = ref(null);
const actionsData = ref([]);

const hideInput = () => {
  showDeposit.value = false;
  showWithdraw.value = false;
  displayButtons.value = true;
  amount.value = null;
}

const displayDepositInput = () => {
  showDeposit.value = true;
  displayButtons.value = false;
}

const displayWithdrawInput = () => {
  showWithdraw.value = true;
  displayButtons.value = false;
}

function formatDate(date) {
  return date.toISOString().split('T')[0];
}

const depositFunds = async(goal_id, user_id, amount) => {
  try {
    const url = new URL("http://localhost:8000/savings/deposit/");
    url.searchParams.append("user_id", user_id);
    url.searchParams.append("goal_id", goal_id);
    url.searchParams.append("amount", amount);
    
    const response = await fetch(url.toString(), {
      method: "PUT"
    });

    if (!response.ok) {
      throw new Error (`HTTP error! Status: ${response.status}`);
    }

  }
  catch (error) {
    console.error(`An error has occured while fetching savings actions data: ${error}`);
  }
}

const postNewGoalAction = async(goal, type, user_id) => {
  try {
    const response = await fetch("http://localhost:8000/savings/new_goal_action/", {
      method: "POST",
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        type: type, 
        amount: parseFloat(amount.value), 
        date: formatDate(new Date()),
        goal_id: goal.id,
        user_id: user_id
      })
    });

    if (!response.ok) {
      throw new Error (`HTTP error! Status: ${response.status}`);
    }
    fetchSavingActions(goal.id, 2);
    depositFunds(goal.id, 2, amount.value);
    amount.value = null;
    hideInput();
  }
  catch (error) {
    console.error(`An error has occured while posting savings actions data: ${error}`);
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

watch(() => goal?.id, (newGoalId) => {
  if (newGoalId) {
    fetchSavingActions(goal.id, 2)
  }
},{ immediate: true });

</script>

<template>
  <div class="w-64 h-96 flex flex-col items-center p-4
  bg-[#E9ECEF] rounded-xl shadow-xl">
    <img :src="goal.cover"
      class="w-[100%] h-[40%] rounded-lg"/>
    <p class="text-xl font-bold text-neutral-800 mt-2">{{ goal.title }}</p>
    <p class="text-3xl font-semibold text-neutral-800" :class="{'line-through': goal.finished === 1}">${{ goal.current_amount }} / ${{ goal.goal_amount }}</p>

    <div class="w-full h-[30%] border-y-2 flex flex-col items-center border-neutral-400 mt-2">
      <p class="text-xs h-1/6 text-neutral-400 font-semibold">Recent actions</p>
      <span v-for="action in actionsData" :key="action.id" class="w-[90%] h-1/6 flex justify-between">
        <p class="text-xs text-neutral-400 font-semibold">{{ action.date }}</p>
        <p class="text-xs text-neutral-400 font-semibold">{{ action.type === 'deposit' ? "+" : "-" }}${{ action.amount }}</p>
      </span>
    </div>

    <span v-if="displayButtons" class="w-[100%] h-[20%] flex justify-between items-end mt-auto">
      <button @click="displayDepositInput" class="w-[48%] h-10 rounded-3xl bg-neutral-800 text-sm text-[#E9ECEF]
      border-neutral-800 border-2 hover:cursor-pointer hover:bg-[#588157]
        transition ease-in-out duration-200">Add funds</button>
      <button @click="displayWithdrawInput" class="w-[48%] h-10 rounded-3xl bg-none font-semibold text-sm text-neutral-800 
       border-neutral-800 border-2 hover:cursor-pointer hover:bg-[#BC4749] hover:text-[#E9ECEF]
        transition ease-in-out duration-200">Withdraw</button>
    </span>

    <span v-if="showDeposit" class="w-[100%] h-[10%] flex items-end justify-between mt-auto">
      <input type="number" placeholder="Deposit amount" v-model="amount"
        class="w-[70%] h-10 px-2 border-2 border-neutral-800 rounded-l-lg border-r-0 text-md font-medium focus:outline-0"
      />
      <button @click="postNewGoalAction(goal, 'deposit', 2)" 
        class="w-[30%] h-10 rounded-r-lg bg-none font-semibold text-sm text-neutral-800 
      border-neutral-800 border-2 hover:cursor-pointer hover:bg-[#588157] hover:text-[#E9ECEF]
        transition ease-in-out duration-200">Confirm</button>
    </span>

    <span v-if="showWithdraw" class="w-[100%] h-[10%] flex items-center justify-between mt-auto">
      <input type="number" placeholder="Withdrawal amount" v-model="amount"
        class="w-[70%] h-full px-2 border-2 border-neutral-800 rounded-l-lg border-r-0 text-md font-medium focus:outline-0"
      />
      <button @click="postNewGoalAction(goal, 'withdraw', 2)" 
        class="w-[30%] h-full rounded-r-lg bg-none font-semibold text-sm text-neutral-800 
      border-neutral-800 border-2 hover:cursor-pointer hover:bg-[#BC4749] hover:text-[#E9ECEF]
        transition ease-in-out duration-200">Confirm</button>
    </span>

     <a v-if="showDeposit || showWithdraw" 
      @click="hideInput"
      class="text-sm text-neutral-800 hover:underline hover:cursor-pointer h-[10%] flex items-center"
    >Cancel</a>
  </div>
</template>