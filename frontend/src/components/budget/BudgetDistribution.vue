<script setup lang="ts">
import { ref, watch, onMounted } from "vue";
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
const { budgetData, budgetShares, fetchBudget, updateBudget, fetchBudgetShares, updateBudgetShares } = useBudget();

const budget = ref<number>(1);
const values = ref<number[] | null>(null);
const originalValues = ref<number[] | null>(null);
const hasChanged = ref<boolean>(false);

// budget value input
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

// get present values for handlers on slider
const calculateInitialShares = () => {
  if (!budgetShares.value || budgetShares.value.length === 0) return;

  const sharesAmounts = budgetShares.value.map(share => share.amount);

  const sliderValues: number[] = [];
  let temp = 0;
  for (let i = 0; i < sharesAmounts.length - 1; i++) {
    temp += sharesAmounts[i];
    sliderValues.push(temp);
  }

  values.value = sliderValues;
  originalValues.value = [...sliderValues];
}

// assign fetched data
const setInitialValues = async () => {
  await fetchExpenseCategories(2);
  await fetchBudget(2, monthId);
  if (!budgetData.value?.id) return;
  await fetchBudgetShares(budgetData.value!.id);
  budget.value = budgetData.value?.amount ?? 1;
  calculateInitialShares();
  hasChanged.value = false;
}

// calculate shares and ranges for categories
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

const handleSaveChanges = async () => {
  if (!values.value || !budgetData.value) return;

  const full = [0, ...values.value, budget.value];

  const newShares = budgetShares.value.map((share, id) => {
    return {
      share_id: share.id,
      amount: Number((full[id+1] - full[id]).toFixed(2))
    }
  });

  await updateBudgetShares(newShares);
  await setInitialValues();
}

// watch changes for budget, update shares
watch(budget, async (newValue, oldValue) => {
  if (newValue != oldValue) {
    await updateBudget(newValue, 2, monthId);
    await fetchBudget(2, monthId);
    getCategoryRanges();
  }
});

// watch changes for shares
watch(values, async (newValue) => {
  if(!newValue || !originalValues.value) return;
  getCategoryRanges();
  hasChanged.value = newValue.some((v, i) => v !== originalValues.value![i]);
});

watch(() => monthId, async (newValue, oldValue) => {
  if (newValue !== oldValue) {
    await setInitialValues();
  }
});

onMounted(async () => {
  await setInitialValues();
});

</script>

<template>
  <div class="w-[48%] h-[60%] bg-[#E9ECEF] flex flex-col p-4 gap-4
    rounded-xl shadow-xl">
    <p class="text-3xl text-[#212529] font-semibold">Budget distribution</p>
    <p v-if="!budgetData?.id" class="text-neutral-400 font-semibold">Cannot modify past budgets.</p>
    <div v-if="budgetData?.id" class="flex items-baseline w-full gap-1">
      <label class="text-neutral-800 text-xl font-semibold">Your budget in {{ getMonthName(monthId.slice(-2)) }}: $</label>
      <input type="number" :value="budget" @input="handleInput" :min="1"
        class="w-24 h-8 focus:outline-2 rounded-xl text-neutral-800 text-xl font-semibold "
      />
    </div>
    <div v-if="budgetData?.id" class="flex flex-col gap-16 w-full">
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
      <div class="w-full flex flex-wrap justify-evenly gap-8 ">
        <p v-for="(cat, index) in expenseCategories" :key="cat.id" 
          class="text-neutral-800 text-md font-semibold">
          {{ cat.name }}: ${{ categoriesValues[index] }} - {{ categoriesShares[index] }}%
        </p>
      </div>
      <div v-if="hasChanged" class="w-full flex justify-around">
        <button @click="setInitialValues"
        class="w-24 h-8 rounded-3xl bg-none font-semibold text-sm text-neutral-800 
        border-neutral-800 border-2 hover:cursor-pointer hover:bg-neutral-800  hover:text-[#E9ECEF]
        transition ease-in-out duration-200">Cancel</button>

        <button @click="handleSaveChanges"
        class="w-32 h-8 rounded-3xl bg-none font-semibold text-sm text-neutral-800 
        border-neutral-800 border-2 hover:cursor-pointer hover:bg-neutral-800  hover:text-[#E9ECEF]
        transition ease-in-out duration-200">Save changes</button>
      </div>
    </div>
  </div>
</template>