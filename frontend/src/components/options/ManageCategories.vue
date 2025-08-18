<script setup lang="ts">
import { onMounted, ref } from "vue";
import useExpenseCategories from "@/composables/useExpenseCategories";

const displayNewCategory = ref<boolean>(false);
const displayDeleteCategory = ref<boolean>(false);
const newCategory = ref<string>("");
const categoryToDelete = ref<number>(0);

const { expenseCategories, fetchExpenseCategories, postNewCategory, deleteCategory } = useExpenseCategories();

const switchDisplayNewCategory = () => {
  displayNewCategory.value = !displayNewCategory.value;
  displayDeleteCategory.value = false;
  newCategory.value = "";
}
const switchDisplayDeleteCategory = () => {
  displayDeleteCategory.value = !displayDeleteCategory.value;
  displayNewCategory.value = false;
}

const handleNewCategory = async () => {
  await postNewCategory(2, newCategory.value);
  await fetchExpenseCategories(2);
  switchDisplayNewCategory();
}

const handleDeleteCategory = async () => {
  await deleteCategory(2, categoryToDelete.value);
  await fetchExpenseCategories(2);
  switchDisplayDeleteCategory();
}

onMounted(async () => {
  await fetchExpenseCategories(2);
});

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
        <button @click="handleNewCategory"
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
        <button @click="handleDeleteCategory"
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