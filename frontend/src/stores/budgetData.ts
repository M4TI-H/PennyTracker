import { ref } from "vue";

export const refreshBudgetData = ref({
  isRefreshed: false,
  refreshNow(value: boolean) {
    this.isRefreshed = value;
  }
});