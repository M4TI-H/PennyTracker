<script setup lang="ts">
import { onMounted, computed } from "vue";
import ExpensesView from "./ExpensesView.vue";
import useTransactions from "@/composables/useTransactions";

defineProps<{ visible: boolean }>();

const emit = defineEmits<{
  (e: "update:visible", value: boolean): void
  (e: "deletion"): void
}>();

const { transactionsData, fetchRecentTransactions } = useTransactions();

const isFull = computed(() => transactionsData.value.length === 4);

//switch display state of all expenses component
const switchShowAll = () => emit("update:visible", true);

const transactionDeletion = async () => {
  await fetchRecentTransactions();
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