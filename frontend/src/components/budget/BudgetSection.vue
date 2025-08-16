<script setup lang="ts">
import { ref, onMounted, watch, nextTick } from "vue";
import BudgetChartDetailed from './BudgetChartDetailed.vue';
import getMonthName from "@/composables/getMonthName";
import BudgetUsage from "./BudgetUsage.vue";
import useBudget from "@/composables/useBudget";

const { categoriesValues, categoriesShares, month } = defineProps<{
  categoriesValues: number[],
  categoriesShares: number[],
  month: string
}>();

const emit = defineEmits<{
  (e: "update:month", payload: string): void;
}>();

const { budgetData, budgetSummaryData, fetchBudget, fetchBudgetSummary } = useBudget();

function getMonths(): { id: number; value: string; month_name: string, year: string }[] {
  const result: { id: number; value: string; month_name: string, year: string }[] = [];
  const now = new Date();

  for (let i = 0; i < 12; i++) {
    const date = new Date(now.getFullYear(), now.getMonth() - i, 1);
    const month_num = (date.getMonth() + 1).toString().padStart(2, "0");
    const month_name = getMonthName(month_num);
    const year = date.getFullYear().toString();

    const value = `${year}-${month_num}`;
    result.push({id: i, value, month_name, year});
  }

  return result;
}

const monthId = ref<string>(month);

watch(monthId, (newValue) => {
  emit("update:month", newValue);
});

onMounted(async () => {
  const now = new Date();
  const current = `${now.getFullYear()}-${(now.getMonth() + 1).toString().padStart(2, "0")}`;
  monthId.value = current;
  emit("update:month", current);

  await fetchBudget(2, current);
  if (!budgetData.value?.id) return;
  await fetchBudgetSummary(budgetData.value.id);
});

</script>

<template>
  <div class="w-[48%] h-full flex flex-col items-center p-4 gap-4 bg-[#E9ECEF] rounded-xl shadow-xl">
    <span class="flex items-center gap-2">
      <p class="text-lg text-neutral-800 font-semibold">Budget in</p>
      <select v-model="monthId" class="h-10 bg-[#FFF] border-2 border-neutral-800 
        rounded-lg font-semibold text-md px-2 focus:outline-0"
      >
        <option v-for="month in getMonths()" :key="month.id" :value="month.value">
          {{ month.month_name }} ({{ month.year }})
        </option>
      </select>
    </span>
    <div class="w-[60%]">
      <BudgetChartDetailed :budgetSummaryData="budgetSummaryData"/>
    </div>
    <BudgetUsage :budgetSummaryData="budgetSummaryData"/>
  </div>
</template>