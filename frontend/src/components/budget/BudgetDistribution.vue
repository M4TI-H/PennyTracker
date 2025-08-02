<script setup lang="ts">
import { ref, watch, onMounted } from "vue";
import Slider from "@vueform/slider";
import getMonthName from "@/composables/getMonthName";
import useExpenseCategories from "@/composables/useExpenseCategories";
import '@vueform/slider/themes/default.css'

const { categoriesValues, categoriesShares, monthId, monthlyBudget } = defineProps<{
  categoriesValues: number[],
  categoriesShares: number[],
  monthlyBudget: number,
  monthId: string,
}>();

const emit = defineEmits<{
  (e: 'update:categoriesValues', payload: number[]): void;
  (e: 'update:categoriesShares', payload: number[]): void;
  (e: 'update:monthlyBudget', payload: number): void;
}>();

const { expenseCategories, fetchExpenseCategories } = useExpenseCategories();

//expenseCategories.length
const budget = ref<number>(monthlyBudget);

const values = ref<number[] | null>(null);

const calculateValues = () => {
  const n = expenseCategories.value.length;
  const step = Math.round(monthlyBudget / n);
  values.value = Array.from({ length: n - 1 }, (_, i) => Math.round((i + 1) * step));
}

const getCategoryRanges = () => {
  if (!values.value) return [];

  const full = [0, ...values.value, monthlyBudget];
  const ranges = [];
  const shares = [];

  for (let i = 0; i < full.length - 1; i++) {
    ranges.push(Number((full[i+1] - full[i]).toFixed(2)));
    shares.push(Number(((full[i+1] - full[i]) * 100 / monthlyBudget).toFixed(2)));
  }

  emit("update:categoriesValues", ranges);
  emit("update:categoriesShares", shares);
};

watch(budget, (newValue) => {
  emit("update:monthlyBudget", newValue);
  getCategoryRanges();
});

watch(values, () => {
  getCategoryRanges();
});

onMounted(async () => {
  await fetchExpenseCategories(2);
  calculateValues();
});

</script>

<template>
  <div class="w-[48%] h-[60%] bg-[#E9ECEF] flex flex-col p-4 gap-4
    rounded-xl shadow-xl">
    <p class="text-3xl text-[#212529] font-semibold">Budget distribution</p>
    <div class="flex items-baseline w-full gap-1">
      <label class="text-neutral-800 text-xl font-semibold">Your budget in {{ getMonthName(monthId) }}: $</label>
      <input type="number" v-model="budget" class="w-24 h-8 focus:outline-2 rounded-xl text-neutral-800 text-xl font-semibold "/>
    </div>
    <div class="flex flex-col gap-16 w-full">
      <p class="text-neutral-600 text-lg font-semibold">Select distribution shares:</p>
       <Slider
        v-if="values"
        v-model="values"
        :min="0"
        :max="budget"
        :tooltips="true"
        :step="1"
        :lazy="true"
        :marks="true"
        class="w-[90%] self-center"
      />
      <div class="w-full flex flex-wrap justify-evenly gap-8">
        <p v-for="(cat, index) in expenseCategories" :key="cat.id" 
          class="text-neutral-800 text-md font-semibold">
          {{ cat.name }}: ${{ categoriesValues[index] }} - {{ categoriesShares[index] }}%
        </p>
      </div>
    </div>
  </div>
</template>