<script setup lang="ts">
import { onMounted, ref, watch } from "vue";
import type { TransactionCountType, MonthInfo } from "@/types/transactions";
import getMonthName from "@/composables/getMonthName";
import { fetchTransactionsCount } from "@/composables/dashboardDataFetches";

const transactionsCountData = ref(<TransactionCountType[]>[]);
const showDetailsOfDay = ref<string | null>(null);
let monthData = ref<MonthInfo[]>([]);

const onTileHoverEnter = (day: string) => {
  showDetailsOfDay.value = day;
}

const onTileHoverLeave = () => {
  showDetailsOfDay.value = null;
}

function getMonthLen(){
  const now = new Date();
  const months = [];

  for (let i = 3; i > 0; i--) {
    const year = now.getFullYear();
    const month = now.getMonth() - i;
    const date = new Date(year, month + 2, 0);

    months.push({
      year: date.getFullYear(),
      month: (date.getMonth() + 1).toString().padStart(2, '0'),
      length: date.getDate()
    });
  }
  return months;
}

function formatDate(day: number | string, month: string, year: number | string) : string {
  return `${day.toString().padStart(2, "0")}/${month}/${year}`;
}

const transactionMap = ref<Record<string, { num: number; level: number }>>({});

watch(() => transactionsCountData.value, (newData) => {
  transactionMap.value = newData.reduce((map, t: TransactionCountType) => {
    const [day, month, year] = t.date.split('/');
    const date = formatDate(day, month, year);

    map[date] = {num: t.number_of_transactions, level: t.level};
    return map;
  }, {} as Record<string, { num: number; level: number }>);
});

function getTransactionsForDay(date: string) {
  return transactionMap.value[date]?.num || 0;
}

function getTransactionLevel(date: string) {
  let level = transactionMap.value[date]?.level;
  return level || 0;
}

function getOpacity(level: number) {
  const opacityLevel = [
    "bg-[#588157]/20",
    "bg-[#588157]/50",
    "bg-[#588157]/70",
    "bg-[#588157]/90",
    "bg-[#588157]/100",
  ]
  return opacityLevel[level];
}

function calculateTransactionLevel(num: number): number {
  if (num === 1) return 1;
  if (num === 2 || num === 3) return 2;
  if (num > 3 && num <= 5) return 3;
  if (num > 5 && num < 10) return 4;
  return 0;
}

onMounted(async() => {
  transactionsCountData.value = await fetchTransactionsCount(2);
  transactionsCountData.value = transactionsCountData.value.map(t => ({
    ...t,
    level: calculateTransactionLevel(t.number_of_transactions)
  }));

  monthData.value = getMonthLen();
})
</script>

<template>
  <div class="max-w-[70%] min-w-128 w-full h-96 bg-[#E9ECEF] rounded-xl shadow-xl flex flex-col items-center justify-evenly">
    <p class="text-neutral-800 text-2xl font-semibold">Monthly transaction count</p>
    <span class="w-full flex items-center justify-center  gap-8">
      <div div v-for="month in monthData" :key="month.month"
        class="w-64 h-72 flex flex-col items-center gap-4"
      >
        <p class="text-neutral-800 text-xl font-semibold">{{ getMonthName(month.month) }}</p>
        <div class="flex flex-wrap gap-1">
          <div v-for="day in month.length" :key="day"
            @mouseenter="onTileHoverEnter(formatDate(day, month.month, month.year))" @mouseleave="onTileHoverLeave"
            class="relative size-8 flex justify-center items-center rounded-md hover:bg-[#588157]/100 hover:cursor-default"
            :class="getOpacity(getTransactionLevel(formatDate(day, month.month, month.year)))"
          > 
            {{ day }}
            <div v-if="showDetailsOfDay === formatDate(day, month.month, month.year)"
              class="absolute w-36 h-14 left-9 z-10
              p-1 bg-neutral-800/95 rounded-lg"
            >
              <p class="text-neutral-400">
                {{ getTransactionsForDay(formatDate(day, month.month, month.year)) }} 
                {{ getTransactionsForDay(formatDate(day, month.month, month.year)) === 1 ? "transaction" : "transactions" }}
                on {{ String(day).padStart(2, "0") }}/{{ month.month }}/{{ month.year }}
              </p>
            </div>
          </div>
        </div>
      </div>
    </span>
  </div>
</template>