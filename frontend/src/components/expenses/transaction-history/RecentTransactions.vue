<script setup>
import { onMounted, ref, computed } from "vue";
import ExpensesView from "./ExpensesView.vue";

defineProps({
  modelValue: Boolean
});

const emit = defineEmits(["update:modelValue", "deletion"]);

const transactionsData = ref([]);
const isFull = computed(() => transactionsData.value.length === 4);

const fetchRecentTransactions = async() => {
  try {
    const response = await fetch("http://localhost:8000/transactions/fetch_recent");
    if (!response.ok) {
      throw new Error (`HTTP error! Status: ${response.status}`);
    }

    transactionsData.value = await response.json();
  }
  catch (error) {
    console.error(`An error has occured while fetching transactions data: ${error}`);
  }
}

//switch display state of all expenses component
const switchShowAll = () => emit('update:modelValue', true);

const transactionDeletion = () => {
  fetchRecentTransactions();
  emit("deletion");
}

defineExpose({
  fetchRecentTransactions
});

onMounted(async () => fetchRecentTransactions());

</script>

<template>
  <div class="sm:w-[59%] h-[38%] flex flex-col items-center bg-[#E9ECEF] p-4 rounded-xl shadow-xl gap-2">
    <p class="text-2xl text-neutral-800 font-semibold mb-2">Recent transactions</p>
    <ExpensesView :transactionsData="transactionsData" @deletion="transactionDeletion"/>
    <a v-if="isFull" @click="switchShowAll"
      class="text-sm text-neutral-400 font-semibold hover:underline hover:cursor-pointer"
    >Show all</a>
  </div>
</template>