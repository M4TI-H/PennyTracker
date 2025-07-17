<script setup>
import { onMounted, ref, watch } from "vue";
const {transactionsCountData} = defineProps({
  transactionsCountData: Array,
});

const showDetailsOfDay = ref(null);

const onTileHoverEnter = (day) => {
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

function formatDate(day, month, year) {
  return `${String(day).padStart(2, "0")}/${month}/${year}`;
}

let monthData = [];
const transactionMap = ref({});

onMounted(() => {
  monthData = getMonthLen();
});

watch(() => transactionsCountData, (newData) => {
  transactionMap.value = transactionsCountData.reduce((map, t) => {
    const [day, month, year] = t.date.split('/');
    const date = formatDate(day, month, year);

    map[date] = {num: t.number_of_transactions, level: t.level};
    return map;
  }, {});
});

function getTransactionsForDay(date) {
  return transactionMap.value[date]?.num || 0;
}

function getTransactionLevel(date) {
  let level = transactionMap.value[date]?.level;
  return level || 0;
}

function getOpacity(level) {
  const opacityLevel = [
    "bg-[#588157]/20",
    "bg-[#588157]/50",
    "bg-[#588157]/70",
    "bg-[#588157]/90",
    "bg-[#588157]/100",
  ]
  return opacityLevel[level];
}

</script>

<template>
  <div class="max-w-[70%] min-w-128 w-full h-96 bg-[#E9ECEF] rounded-xl shadow-xl flex items-center justify-center gap-8">
    <div v-for="month in monthData" :key="month.month"
      class="w-64 h-72 flex flex-col items-center gap-4"
    >
      <p class="text-neutral-800 text-xl font-semibold">{{ month.month }}</p>
      <div class="flex flex-wrap gap-1">
        <div v-for="day in month.length" :key="day"
          @mouseenter="onTileHoverEnter(formatDate(day, month.month, month.year))" @mouseleave="onTileHoverLeave"
          class="relative size-8 flex justify-center items-center hover:bg-[#588157]/100 hover:cursor-default"
          :class="getOpacity(getTransactionLevel(formatDate(day, month.month, month.year)))"
        > 
          {{ day }}
          <div v-if="showDetailsOfDay === formatDate(day, month.month, month.year)"
            class="absolute w-36 h-14 left-8 z-10
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
  </div>
</template>