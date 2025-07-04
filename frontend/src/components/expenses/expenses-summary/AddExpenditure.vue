<script setup>
import { ref } from "vue";
import formatDate from "@/composables/formatDate";

defineProps({
  expenseCategories: Array,
  paymentMethods: Array
});

const data = ref({
  name: "",
  amount: null,
  method: "",
  category: null,
  user_id: 2
});

const emit = defineEmits(["after-submit"]);

const postNewExpenditure = async() => {
  console.table(data.value);
  try {
    const response = await fetch("http://localhost:8000/transactions/new_expenditure/", {
      method: "POST",
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        name: data.value.name, 
        amount: data.value.amount ? parseFloat(data.value.amount) : 0,
        method: data.value.method, 
        category: data.value.category ? parseInt(data.value.category) : -1,
        date: formatDate(new Date()).slice(0, 10),
        user_id: data.value.user_id
      })
    });

    if (!response.ok) {
      const err = await response.json()
      throw new Error(err.detail); 
    }

    data.value = {
      name: "",
      amount: null,
      method: "",
      category: null,
      user_id: 2
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
      v-model="data.name"
    />
    <input type="number" placeholder="Amount" 
      class="w-[70%] h-10 bg-[#FFF] border-2 border-neutral-800 rounded-lg font-semibold text-md px-2 focus:outline-0"
      v-model="data.amount"
    />
    <span class="w-[70%] h-10 flex justify-between items-center">
      <p class="text-md text-neutral-800 font-semibold">Method:</p>
      <select class="w-[60%] h-10 bg-[#FFF] border-2 border-neutral-800 rounded-lg font-semibold text-md px-2 focus:outline-0"
        v-model="data.method"
      >
        <option v-for="method in paymentMethods" :key="method.id">{{ method.name }}</option>
      </select>
    </span>
    <span class="w-[70%] h-10 flex justify-between items-center">
      <p class="text-md text-neutral-800 font-semibold">Category:</p>
      <select class="w-[60%] h-10 bg-[#FFF] border-2 border-neutral-800 rounded-lg font-semibold text-md px-2 focus:outline-0"
        v-model="data.category"
      >
        <option :value="category.id" v-for="category in expenseCategories" :key="category.id">{{ category.name }}</option>
      </select>
    </span>
    <button @click="postNewExpenditure"
      class="w-[50%] h-10 rounded-3xl bg-neutral-800 text-sm text-[#E9ECEF]
    border-neutral-800 border-2 hover:cursor-pointer hover:bg-[#588157]
      transition ease-in-out duration-200">Confirm</button>
  </div>
</template>