<script setup>
defineProps({
  transactionsData: Array
});

const emit = defineEmits(["deletion"]);

const deleteTransaction = async(user_id, transaction) => {
  try {
    const url = new URL("http://localhost:8000/transactions/delete_one");
    url.searchParams.append("user_id", user_id);
    url.searchParams.append("transaction_id", transaction);

    const response = await fetch(url.toString(), {
      method: "DELETE"
    });

    if (!response.ok) {
      throw new Error (`HTTP error! Status: ${response.status}`);
    }

    emit("deletion");
  }
  catch (error) {
     console.error(`An error has occured while deleting a transaction: ${error}`);
  }
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
    <p class="w-[15%] text-sm text-neutral-800 font-semibold">{{ expense.method }}</p>
    <p class="w-[15%] text-sm text-neutral-800 font-semibold">{{ expense.date }}</p>
    <button @click="deleteTransaction(2, expense.id)" class="w-[5%] hover:cursor-pointer transition ease-in-out duration-200 hover:scale-120"><i class="pi pi-trash"></i></button>
  </div>
</template>