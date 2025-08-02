<script setup lang="ts">
import { ref, watch, onMounted, computed, warn } from "vue";
import Slider from "@vueform/slider";
import getMonthName from "@/composables/getMonthName";
import useExpenseCategories from "@/composables/useExpenseCategories";
import '@vueform/slider/themes/default.css'
import useBudget from "@/composables/useBudget";

const { categoriesValues, categoriesShares, monthId } = defineProps<{
  categoriesValues: number[],
  categoriesShares: number[],
  monthId: string,
}>();

const emit = defineEmits<{
  (e: 'update:categoriesValues', payload: number[]): void;
  (e: 'update:categoriesShares', payload: number[]): void;
}>();

const { expenseCategories, fetchExpenseCategories } = useExpenseCategories();
const { budgetData, fetchBudget, updateBudget } = useBudget();

//expenseCategories.length
const budget = ref<number>(1);
const values = ref<number[] | null>(null);

onMounted(async () => {
  await fetchExpenseCategories(2);
  await fetchBudget(2, monthId);
  budget.value = budgetData.value?.amount ?? 1;
  calculateValues();
});

watch(budget, async (newValue, oldValue) => {
  if (newValue != oldValue) {
    await updateBudget(newValue, 2, monthId);
    await fetchBudget(2, monthId);
    calculateValues();
  }
});

const calculateValues = () => {
  const n = expenseCategories.value.length;
  const step = Math.round(budget.value / n);
  values.value = Array.from({ length: n - 1 }, (_, i) => Math.round((i + 1) * step));
}

const getCategoryRanges = () => {
  if (!values.value || budget.value === 0) return [];

  const full = [0, ...values.value, budget.value];
  const ranges = [];
  const shares = [];

  for (let i = 0; i < full.length - 1; i++) {
    ranges.push(Number((full[i+1] - full[i]).toFixed(2)));
    shares.push(Number(((full[i+1] - full[i]) * 100 / budget.value).toFixed(2)));
  }

  emit("update:categoriesValues", ranges);
  emit("update:categoriesShares", shares);
};

const handleInput = (e: Event) => {
  const target = e.target as HTMLInputElement;

  if (target.value === "") {
    budget.value = 1;
  }
  else{
    if (Number(target.value) < 1) {
      budget.value = 1;
    }
    else{
      budget.value = Number(target.value);
    }
  }
}

watch(values, () => {
  getCategoryRanges();
});

</script>

<template>
  <div class="w-[48%] h-[60%] bg-[#E9ECEF] flex flex-col p-4 gap-4
    rounded-xl shadow-xl">
    <p class="text-3xl text-[#212529] font-semibold">Budget distribution</p>
    <div class="flex items-baseline w-full gap-1">
      <label class="text-neutral-800 text-xl font-semibold">Your budget in {{ getMonthName(monthId) }}: $</label>
      <input type="number" :value="budget" @input="handleInput" :min="1"
        class="w-24 h-8 focus:outline-2 rounded-xl text-neutral-800 text-xl font-semibold "
      />
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