<script setup>
import { ref } from "vue";
const {transactionsCountData} = defineProps({
  transactionsCountData: Array,
});

const showDetails = ref(false);

const onTileHoverEnter = () => {
  showDetails.value = true;
}

const onTileHoverLeave = () => {
  showDetails.value = false;
}

</script>

<template>
  <div class="max-w-[60%] sm:max-w-[70%] w-full sm:min-w-128 sm:h-96 bg-[#E9ECEF] p-4 rounded-xl shadow-xl">
    <div v-for="transaction in transactionsCountData" :key="transaction.id"
      @mouseenter="onTileHoverEnter" @mouseleave="onTileHoverLeave"
      class="size-6 bg-red-500"
    >
      <p v-if="showDetails"
      >
        Date: {{ transaction.date }}
      </br>
        Transactions: {{ transaction.number_of_transactions }}
      </p>
    </div>
  </div>
</template>