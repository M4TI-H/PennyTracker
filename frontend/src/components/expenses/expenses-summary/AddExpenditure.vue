<script setup lang="ts">
import { ref } from "vue";
import formatDate from "@/composables/formatDate";
import type { Category, Account } from "@/types/options";
import type { NewTransaction } from "@/types/transactions";

const { expenseCategories, accountsData } = defineProps<{
  expenseCategories: Category[],
  accountsData: Account[]
}>();

const newExpData = ref<NewTransaction>({
  name: undefined,
  amount: undefined,
  method: undefined,
  category: undefined,
});

const emit = defineEmits(["after-submit"]);

const postNewExpenditure = async(user_id: number) => {
  try {
    const response = await fetch("http://localhost:8000/transactions/new_expenditure/", {
      method: "POST",
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        name: newExpData.value.name, 
        amount: newExpData.value.amount ? newExpData.value.amount : 0,
        method: newExpData.value.method ? newExpData.value.method : -1, 
        category: newExpData.value.category ? newExpData.value.category : -1,
        date: formatDate(new Date()).slice(0, 10),
        user_id: user_id
      })
    });

    if (!response.ok) {
      const err = await response.json()
      throw new Error(err.detail); 
    }

    newExpData.value = {
      name: undefined,
      amount: undefined,
      method: undefined,
      category: undefined,
    };

    emit("after-submit");
  }
  catch (error) {
    console.error(`An error has occured while posting transactions data: ${error}`);
  }
}
</script>
<template>
  <div class="w-[25%] flex flex-col items-center gap-6">
    <p class="text-2xl text-neutral-800 font-semibold">New expenditure</p>
    <input type="text" placeholder="Name of expense" 
      class="w-[70%] h-10 bg-[#FFF] border-2 border-neutral-800 rounded-lg font-semibold text-md px-2 focus:outline-0"
      v-model="newExpData.name"
    />
    <input type="number" placeholder="Amount" 
      class="w-[70%] h-10 bg-[#FFF] border-2 border-neutral-800 rounded-lg font-semibold text-md px-2 focus:outline-0"
      v-model="newExpData.amount"
    />
    <span class="w-[70%] h-10 flex justify-between items-center">
      <p class="text-md text-neutral-800 font-semibold">Method:</p>
      <select class="w-[60%] h-10 bg-[#FFF] border-2 border-neutral-800 rounded-lg font-semibold text-md px-2 focus:outline-0"
        v-model="newExpData.method"
      >
        <option v-for="method in accountsData" :key="method.id" :value="method.id">{{ method.name }}</option>
      </select>
    </span>
    <span class="w-[70%] h-10 flex justify-between items-center">
      <p class="text-md text-neutral-800 font-semibold">Category:</p>
      <select class="w-[60%] h-10 bg-[#FFF] border-2 border-neutral-800 rounded-lg font-semibold text-md px-2 focus:outline-0"
        v-model="newExpData.category"
      >
        <option :value="category.id" v-for="category in expenseCategories" :key="category.id">{{ category.name }}</option>
      </select>
    </span>
    <button @click="postNewExpenditure(2)"
      class="w-[50%] h-10 rounded-3xl bg-neutral-800 text-sm text-[#E9ECEF]
    border-neutral-800 border-2 hover:cursor-pointer hover:bg-[#588157]
      transition ease-in-out duration-200">Confirm</button>
  </div>
</template>