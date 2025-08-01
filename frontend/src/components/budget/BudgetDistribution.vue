<script setup lang="ts">
import { ref, computed, onMounted } from "vue";
import Slider from "@vueform/slider";
import getMonthName from "@/composables/getMonthName";
import useExpenseCategories from "@/composables/useExpenseCategories";
import '@vueform/slider/themes/default.css'

const { expenseCategories, fetchExpenseCategories } = useExpenseCategories();

const monthlyBudget = ref<number>(1000);
const values = ref([0, 200, 550]);

onMounted(() => fetchExpenseCategories(2));

</script>

<template>
  <div class="w-[48%] h-[60%] bg-[#E9ECEF] flex flex-col p-4 gap-4
    rounded-xl shadow-xl">
    <p class="text-3xl text-[#212529] font-semibold">Budget distribution</p>
    <span class="flex items-baseline w-full gap-1">
      <label class="text-neutral-800 text-xl font-semibold">Your budget in {{ getMonthName((new Date().getMonth() + 1).toString()) }}: $</label>
      <input type="number" v-model="monthlyBudget" class="w-24 h-8 focus:outline-2 rounded-xl text-neutral-800 text-xl font-semibold "/>
    </span>
    <div class="flex flex-col gap-8 w-full h-60 outline-2">
      <p class="text-neutral-600 text-lg font-semibold">Select distribution values:</p>
      <Slider v-model="values" :min="0" :max="monthlyBudget" :step="1" :merge="0"
      class="w-[90%] self-center"/>
    </div>
  </div>
</template>