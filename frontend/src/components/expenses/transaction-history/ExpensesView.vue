<script setup lang="ts">
import useTransactions from '@/composables/useTransactions';
import type { Transaction } from '@/types/transactions';
import { onMounted } from 'vue';

const { transactionsData } = defineProps<{
  transactionsData: Transaction[]
}>();

const emit = defineEmits<{
  (e: "deletion"): void
}>();

const { deleteTransaction } = useTransactions();

const handleDelete = async (user_id: number, transaction_id: number) => {
  await deleteTransaction(user_id, transaction_id);
  emit("deletion");
}

</script>

<template>
  <div class="w-full h-8 flex items-center justify-evenly px-2">
    <p class="w-[15%] text-md text-neutral-800 font-bold">Amount</p>
    <p class="w-[25%] text-md text-neutral-800 font-bold">Title</p>
    <p class="w-[20%] text-md text-neutral-800 font-bold">Category</p>
    <p class="w-[15%] text-md text-neutral-800 font-bold">Method</p>
    <p class="w-[15%] text-md text-neutral-800 font-bold">Date</p>
    <p class="w-[5%] text-md text-neutral-800 font-bold">Action</p>
  </div>
  <div v-for="expense in transactionsData" :key="expense.id" class="w-full h-8 flex items-center justify-evenly px-2">
    <p class="w-[15%] text-sm text-neutral-800 font-semibold">${{ expense.amount }}</p>
    <p class="w-[25%] text-sm text-neutral-800 font-semibold">{{ expense.name }}</p>
    <p class="w-[20%] text-sm text-neutral-800 font-semibold">{{ expense.category_name }}</p>
    <p class="w-[15%] text-sm text-neutral-800 font-semibold">{{ expense.method_name }}</p>
    <p class="w-[15%] text-sm text-neutral-800 font-semibold">{{ expense.date }}</p>
    <button @click="handleDelete(2, expense.id)" class="w-[5%] hover:cursor-pointer transition ease-in-out duration-200 hover:scale-120"><i class="pi pi-trash"></i></button>
  </div>
</template>