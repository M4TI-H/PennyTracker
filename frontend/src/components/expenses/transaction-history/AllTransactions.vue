<script setup lang="ts">
import { ref, onMounted } from 'vue';
import ExpensesView from './ExpensesView.vue';
import type { Transaction } from '@/types/transactions';

defineProps<{ visible: boolean }>();
const emit = defineEmits<{
  (e: "update:visible", value: boolean): void
  (e: "deletion"): void
}>();

const transactionsData = ref<Transaction[]>([]);

const fetchTransactions = async() => {
  try {
    const response = await fetch("http://localhost:8000/transactions/fetch_all");
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
const switchShowAll = () => emit("update:visible", false);

const transactionDeletion = () => {
  fetchTransactions();
  emit("deletion");
}

onMounted(() => fetchTransactions());

</script>

<template>
  <div @click="switchShowAll" class="absolute w-[100%] h-[100vh] bg-neutral-800/70">
    <div @click.stop class="relative top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2
      sm:w-[50%] h-auto min-h-64 max-h-128 flex flex-col items-center bg-[#E9ECEF] p-4 rounded-xl shadow-xl gap-2"
    >
      <p class="text-2xl text-neutral-800 font-semibold mb-2">All transactions</p>
      <button @click="switchShowAll"
        class="absolute right-5 top-3 hover:cursor-pointer"
      >
        <i class="pi pi-times"></i>
      </button>
      <div class="w-full overflow-y-auto">
        <ExpensesView :transactionsData="transactionsData" @deletion="transactionDeletion"/>
      </div>
    </div>
  </div>
</template>