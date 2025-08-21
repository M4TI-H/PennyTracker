<script setup lang="ts">
import { ref, onMounted, watch, nextTick, computed } from "vue";
import BudgetChartDetailed from './BudgetChartDetailed.vue';
import getMonthName from "@/composables/getMonthName";
import BudgetUsage from "./BudgetUsage.vue";
import useBudget from "@/composables/useBudget";
import { refreshBudgetData } from "@/stores/budgetData";

const emit = defineEmits<{
  (e: "update:month", payload: string): void,
}>();

const { budgetData, budgetSummaryData, fetchBudget, fetchBudgetSummary, checkExistenceOfBudget, 
  currentBudgetExists, createNewBudget, budgetMonths, fetchBudgetMonths } = useBudget();
const monthId = ref<string>("");
const displayCreateBudget = ref<boolean>(false);
const budgetExceedAmount = ref<number>(0);

const currentMonth = computed(() => {
  const now = new Date();
  const year = now.getFullYear();
  const month = (now.getMonth() + 1).toString().padStart(2, "0");
  return `${year}-${month}`;
});

function getMonths() {
  if (!budgetMonths.value.length) return [];

  return budgetMonths.value.map(month => {
    const [year, month_num] = month.split("-");
    const month_name = getMonthName(month_num);

    return { month_num, month_name, year };
  });
}

const assignBudgetExceed = (amount: number) => {
  budgetExceedAmount.value = amount;
}

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

watch(() => refreshBudgetData.value.isRefreshed, async (newValue) => {
  if (newValue) {
    if (!budgetData.value?.id) return;
    await fetchBudgetSummary(budgetData.value.id);
    refreshBudgetData.value.refreshNow(false);

    await fetchBudget(2, monthId.value);
    await fetchBudgetSummary(budgetData.value.id);
  }
});

onMounted(async () => {
  await checkExistenceOfBudget(2, currentMonth.value);
  if (!currentBudgetExists.value) {
    monthId.value = currentMonth.value;
    displayCreateBudget.value = true;
    return;
  }

  await fetchBudgetMonths(2);

  const monthsList = getMonths();
  const available = `${monthsList[0].year}-${monthsList[0].month_num}`;
  monthId.value = currentMonth.value;

  emit("update:month", available);

  await fetchBudget(2, available);
  if (!budgetData.value?.id) return;
  await fetchBudgetSummary(budgetData.value.id);
});

</script>

<template>
  <div class="w-[48%] h-full flex flex-col items-center p-4 gap-4 bg-[#E9ECEF] rounded-xl shadow-xl">
    <span v-if="budgetMonths.length > 0" class="flex items-center gap-2">
      <p class="text-lg text-neutral-800 font-semibold">Budget in</p>
      <select v-model="monthId" class="h-10 bg-[#FFF] border-2 border-neutral-800 
        rounded-lg font-semibold text-md px-2 focus:outline-0"
      >
        <option v-for="(month, id) in getMonths()" :key="id" :value="`${month.year}-${month.month_num}`">
          {{ month.month_name }} ({{ month.year }})
        </option>
      </select>
    </span>

    <p v-if="budgetExceedAmount">Budget has been exceeded by ${{ budgetExceedAmount }}!</p>

    <div v-if="budgetData?.id" class="w-[60%]">
      <BudgetChartDetailed   :key="budgetData?.id + '-' + JSON.stringify(budgetSummaryData)"  :budgetData="budgetData" :budgetSummaryData="budgetSummaryData" @budgetExceed="assignBudgetExceed"/>
    </div>

    <BudgetUsage v-if="budgetData?.id" :budgetSummaryData="budgetSummaryData"/>
    <p v-if="!budgetData?.id" class="text-neutral-400 font-semibold">No data</p>
    <div v-if="monthId === currentMonth && !currentBudgetExists">
      <button @click="createNewBudget(2, monthId)"
        class="w-52 h-10 bg-neutral-800 text-neutral-100 font-semibold rounded-2xl hover:cursor-pointer hover:bg-neutral-900"
      >Create budget for {{ getMonthName(monthId.slice(5,7)) }}</button>
    </div>
  </div>
</template>