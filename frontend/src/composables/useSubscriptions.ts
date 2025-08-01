import { ref } from "vue";
import type { Subscription, NewSubscription } from "@/types/transactions";
import formatDate from "./formatDate";

export default function useSubscriptions() {
  const subscriptionsData = ref<Subscription[]>([]);
  const errorMsg = ref<string>("");
  const loading = ref<boolean>(false);

  const fetchSubscriptions = async(user_id: number) => {
    loading.value = true;
    try {
      const response = await fetch("http://localhost:8000/subscriptions/fetch_all");
      
      if (!response.ok) {
        throw new Error (`HTTP error! Status: ${response.status}`);
      }

      subscriptionsData.value = await response.json();
    }
    catch (error: any) {
      errorMsg.value = error.message;
      console.error(`An error has occured while fetching transactions data: ${error}`);
    }
    loading.value = false;
  }

  const postNewSubscription = async(newSubData: NewSubscription, user_id: number) => {
    loading.value = true;
    try {
      const response = await fetch("http://localhost:8000/subscriptions/new_subscription/", {
        method: "POST",
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          service: newSubData.service, 
          amount: newSubData.amount, 
          start_date: formatDate(new Date(newSubData.start_date)).slice(0, 10),
          frequency: newSubData.frequency,
          user_id: user_id
        })
      });

      if (!response.ok) {
        throw new Error (`HTTP error! Status: ${response.status}`);
      }
     
    }
    catch (error: any) {
      errorMsg.value = error.message;
      console.error(`An error has occured while posting subscriptions data: ${error}`);
    }

    loading.value = false;
  }

  const deleteSubscription = async(user_id: number, subscription: number) => {
    loading.value = true;
    try {
      const url = new URL("http://localhost:8000/subscriptions/delete_one");
      url.searchParams.append("user_id", user_id.toString());
      url.searchParams.append("subscription_id", subscription.toString());

      const response = await fetch(url.toString(), {
        method: "DELETE"
      });

      if (!response.ok) {
        throw new Error (`HTTP error! Status: ${response.status}`);
      }

    }
    catch (error: any) {
      errorMsg.value = error.message;
      console.error(`An error has occured while deleting a subscription: ${error}`);
    }

    loading.value = false;
  }

  const calculateNextPayment = (startDate: string, frequency: string) => {
    const now = new Date();
    let nextDate = new Date(startDate);

    while (nextDate <= now) {
      switch (frequency) {
        case "Daily":
          nextDate.setDate(nextDate.getDate() + 1);
          break;
        case "Weekly":
          nextDate.setDate(nextDate.getDate() + 7);
          break;
        case "Monthly":
          nextDate.setMonth(nextDate.getMonth() + 1);
          break;
        case "yearly":
          nextDate.setFullYear(nextDate.getFullYear() + 1);
          break;
      }
    }

    return formatDate(nextDate);
  }

  return {
    subscriptionsData,
    errorMsg,
    loading,
    fetchSubscriptions,
    postNewSubscription,
    deleteSubscription,
    calculateNextPayment
  }
}