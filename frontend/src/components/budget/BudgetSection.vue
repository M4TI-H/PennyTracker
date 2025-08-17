<script setup lang="ts">
import { ref, onMounted, watch, nextTick } from "vue";
import BudgetChartDetailed from './BudgetChartDetailed.vue';
import getMonthName from "@/composables/getMonthName";
import BudgetUsage from "./BudgetUsage.vue";
import useBudget from "@/composables/useBudget";

const { refreshData } = defineProps<{
  refreshData: boolean
}>();

const emit = defineEmits<{
  (e: "update:month", payload: string): void,
  (e: "resetRefresh"): void
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

const monthId = ref<string>("");

watch(monthId, async (newValue, oldValue) => {
  if (newValue === oldValue) return;

  emit("update:month", newValue);

  fetchBudget(2, newValue);


  await nextTick();
  if (budgetData.value?.id) {
    await fetchBudgetSummary(budgetData.value.id);
  } else {
    budgetSummaryData.value = [];
  }
});

watch(() => refreshData, async (newValue) => {
  if (newValue) {
    if (!budgetData.value?.id) return;
    await fetchBudgetSummary(budgetData.value.id);

    emit("resetRefresh");
  }
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
    <div v-if="budgetData?.id" class="w-[60%]">
      <BudgetChartDetailed :budgetSummaryData="budgetSummaryData"/>
    </div>
    <BudgetUsage v-if="budgetData?.id" :budgetSummaryData="budgetSummaryData"/>
    <p v-if="!budgetData?.id" class="text-neutral-400 font-semibold">No data</p>
  </div>
</template>