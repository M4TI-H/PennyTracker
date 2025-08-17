import { ref } from "vue";
import type { Subscription, NewSubscription } from "@/types/transactions";
import formatDate from "./formatDate";
import { fetchData } from "./useFetchData";

export default function useSubscriptions() {
  const subscriptionsData = ref<Subscription[]>([]);
  const errorMsg = ref<string>("");
  const loading = ref<boolean>(false);

  const fetchSubscriptions = async(user_id: number) => {
    loading.value = true;

    const { data, error } = await fetchData<Subscription[]>("http://localhost:8000/subscriptions/fetch_all");
    if (error) errorMsg.value = error;      
    else subscriptionsData.value = data ?? [];

    loading.value = false;
  }

  const postNewSubscription = async(newSubData: NewSubscription, user_id: number) => {
    loading.value = true;

      const { error } = await fetchData<NewSubscription>("http://localhost:8000/subscriptions/new_subscription/", {
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
    
    if (error) errorMsg.value = error;      

    loading.value = false;
  }

  const deleteSubscription = async(user_id: number, subscription: number) => {
    loading.value = true;

    const url = new URL("http://localhost:8000/subscriptions/delete_one");
    url.searchParams.append("user_id", user_id.toString());
    url.searchParams.append("subscription_id", subscription.toString());

     const { error } = await fetchData<Subscription>(url.toString(), {
      method: "DELETE"
    });

    if (error) errorMsg.value = error;    

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