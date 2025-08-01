<script setup lang="ts">
import { computed, ref } from 'vue';
import type { GoalType } from '@/types/savings';
import useSavings from '@/composables/useSavings';

const {showWithdraw, showDeposit, goal} = defineProps<{
  showWithdraw: boolean,
  showDeposit: boolean,
  goal: GoalType
}>();

const emit = defineEmits(["close", "post-action"]);

const { postNewGoalAction } = useSavings();
const amount = ref<number | null>(null);

const action = computed<string | null>(() => {
  if (showDeposit) return 'deposit';
  else if (showWithdraw) return 'withdraw';
  else return null;
});

const handlePostAction = async () => {
  const inputAmount = amount.value;
  if (!inputAmount) {
    console.log("Insert amount!");
    return;
  }

  if (await postNewGoalAction(action.value!, inputAmount, goal) === "success") {
    emit("post-action", { amount: amount.value, action: action.value });
  }
  amount.value = null;
}

const onClose = () => {
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
        <button @click="handlePostAction"
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