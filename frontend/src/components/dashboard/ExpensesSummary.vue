<script setup>
const { monthlyTransactionsData } = defineProps({
  monthlyTransactionsData: Array
});

function formatDate(date) {
  const [year, month] = date.split("-");
  const formattedDate = new Date(year, parseInt(month, 10) - 1);
  return formattedDate.toLocaleString("en-US", { month: "long", year: "numeric" });
}

</script>

<template>
  <div class="w-full sm:w-[60%] max-h-[45%] min-h-32 h-full sm:h-96 bg-[#E9ECEF] p-4 rounded-xl shadow-xl
    flex flex-col items-center"
  >
    <p v-for="month in monthlyTransactionsData"> {{ formatDate(month.month) }} - ${{ month.total_expenses }}</p>
  </div>
</template>