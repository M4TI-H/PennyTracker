<script setup>
const props = defineProps({
  account: Object
});

const emit = defineEmits(["delete"]);

const deleteAccount = async (account_id, user_id) => {
  try {
    const url = new URL("http://localhost:8000/transactions/delete_account/");
    url.searchParams.append("account_id", account_id);
    url.searchParams.append("user_id", user_id);

    const response = await fetch(url.toString(), {
      method: "DELETE"
    });

    if (!response.ok) {
      throw new Error (`HTTP error! Status: ${response.status}`);
    }

    emit("delete");
  }
  catch (error) {
     console.error(`An error has occured while deleting an account: ${error}`);
  }
}

</script>

<template>
  <div class="w-64 h-32 flex flex-col p-4 justify-between
    rounded-xl shadow-xl bg-[#E9ECEF]"
  >
    <span class="w-full flex justify-between items-center">
      <p class="text-md sm:text-xl text-[#212529] font-semibold">{{ account.name }}</p>
      <div>
        <button @click="deleteAccount(account.id, 2)"
          class="text-xl hover:scale-110 hover:cursor-pointer transition ease-in-out duration-200"
        ><i class="pi pi-trash"></i></button>
      </div>
    </span>
    <p class="text-xs text-neutral-400 mt-4">Spent this month</p>
    <span class="flex items-end justify-end h-10">
      <p class="text-2xl sm:text-4xl text-[#212529] font-bold">
        ${{ parseFloat(account.expenses).toFixed(2).split('.')[0] }}
      </p>
      <p class="text-md sm:text-xl text-[#212529] font-semibold">
        .{{ parseFloat(account.expenses).toFixed(2).split('.')[1] }}
      </p>
    </span>
  </div>
</template>