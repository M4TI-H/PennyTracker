<script setup>
import { ref, watchEffect } from "vue";
const displayNewCategory = ref(false);
const displayDeleteCategory = ref(false);
const newCategory = ref("");
const categoryToDelete = ref(0);
const expenseCategories = ref([]);

const fetchExpenseCategories = async() => {
  try {
    const response = await fetch("http://localhost:8000/transactions/expense_categories");
    if (!response.ok) {
      throw new Error (`HTTP error! Status: ${response.status}`);
    }
    expenseCategories.value = await response.json();
  }
  catch (error) {
    console.error(`An error has occured while fetching categories data: ${error}`);
  }
}

const postNewCategory = async (user_id) => {
  try {
    const response = await fetch("http://localhost:8000/transactions/new_category/", {
      method: "POST",
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        name: newCategory.value,
        user_id: user_id
      })
    });

    if (!response.ok) {
      const err = await response.json()
      throw new Error(err.detail); 
    }

    fetchExpenseCategories();
    switchDisplayNewCategory();
  }
  catch (error) {
    console.error(`An error has occured while posting new category: ${error}`);
  }
}

const deleteCategory = async (user_id) => {
  try {
    const url = new URL("http://localhost:8000/transactions/delete_category/");
    url.searchParams.append("category_id", categoryToDelete.value);
    url.searchParams.append("user_id", user_id);

    const response = await fetch(url.toString(), {
      method: "DELETE"
    });

    if (!response.ok) {
      throw new Error (`HTTP error! Status: ${response.status}`);
    }

    fetchExpenseCategories();
    switchDisplayDeleteCategory();
  }
  catch (error) {
     console.error(`An error has occured while deleting a category: ${error}`);
  }
}

watchEffect(() => fetchExpenseCategories());

const switchDisplayNewCategory = () => {
  displayNewCategory.value = !displayNewCategory.value;
  displayDeleteCategory.value = false;
  newCategory.value = "";
}
const switchDisplayDeleteCategory = () => {
  displayDeleteCategory.value = !displayDeleteCategory.value;
  displayNewCategory.value = false;
}
</script>

<template>
  <div class="w-[30%] h-[40%] flex flex-col items-center bg-[#E9ECEF] p-4 rounded-xl shadow-xl">
    <p class="text-xl text-neutral-800 font-semibol">Manage expense categories</p>
    <!--New category form-->
    <span class="w-full h-10 mt-4 flex justify-center">
      <button @click="switchDisplayNewCategory" class="w-40 h-full rounded-3xl bg-neutral-800 text-sm text-[#E9ECEF]
        border-neutral-800 border-2 hover:cursor-pointer transition ease-in-out duration-200"
        :class="{'hidden': displayNewCategory}"
      >Add new category</button>
      <span :class="{'hidden': !displayNewCategory}" class="w-full h-full flex justify-between">
        <input type="text" v-model="newCategory" placeholder="Category name"
          class="w-[50%] h-full bg-[#FFF] border-2 border-neutral-800 rounded-lg font-semibold text-md px-2 focus:outline-0"
        />
        <button @click="postNewCategory(2)"
          class="w-[20%] h-full rounded-3xl bg-neutral-800 text-sm text-[#E9ECEF]
          border-neutral-800 border-2 hover:cursor-pointer transition ease-in-out duration-200"
        >Confirm</button>
        <button @click="switchDisplayNewCategory" class="w-[20%] h-full rounded-3xl bg-none text-sm text-neutral-800
          border-neutral-800 border-2 hover:cursor-pointer transition ease-in-out duration-200"
        >Cancel</button>
      </span>
    </span>
    <!--Category to delete-->
    <span class="w-full h-10 mt-4 flex justify-center">
      <button @click="switchDisplayDeleteCategory" class="w-40 h-full rounded-3xl bg-neutral-800 text-sm text-[#E9ECEF]
        border-neutral-800 border-2 hover:cursor-pointer transition ease-in-out duration-200"
        :class="{'hidden': displayDeleteCategory}"
      >Delete category</button>
      <span :class="{'hidden': !displayDeleteCategory}" class="w-full h-full flex justify-between">
        <select v-model="categoryToDelete"
          class="w-[50%] h-10 bg-[#FFF] border-2 border-neutral-800 rounded-lg font-semibold text-md px-2 focus:outline-0"
        >
          <option v-for="category in expenseCategories" :key="category.id" :value="category.id">{{ category.name }}</option>
        </select>
        <button @click="deleteCategory(2)"
          class="w-[20%] h-full rounded-3xl bg-neutral-800 text-sm text-[#E9ECEF]
          border-neutral-800 border-2 hover:cursor-pointer transition ease-in-out duration-200"
        >Confirm</button>
        <button @click="switchDisplayDeleteCategory" class="w-[20%] h-full rounded-3xl bg-none text-sm text-neutral-800
          border-neutral-800 border-2 hover:cursor-pointer transition ease-in-out duration-200"
        >Cancel</button>
      </span>
    </span>
  </div>
</template>