<script setup lang="ts">
import useAccounts from '@/composables/useAccounts';
import type { Account } from '@/types/options';

const { account } = defineProps<{
  account: Account
}>();

const emit = defineEmits<{
 (e: "refresh"): void
}>();

const { deleteAccount, changeActivity } = useAccounts();

const handleDelete = async () => {
  await deleteAccount(account.id, 2);
  emit("refresh");
}

const handleActivity = async () => {
  let activity = -1;
  if (account.isActive === 1) activity = 0;
  else activity = 1;
  
  await changeActivity(account.id, 2, activity);
  emit("refresh");
}

</script>

<template>
  <div class="w-64 h-32 flex flex-col p-4 justify-between
    rounded-xl shadow-xl bg-[#E9ECEF]"
  >
    <span class="w-full flex justify-between items-center">
      <p v-if="account.isActive === 1" class="text-md sm:text-xl text-[#212529] font-semibold">{{ account.name }}</p>
      <p v-else class="text-md sm:text-xl text-[#212529] font-semibold line-through">{{ account.name }}</p>
      <div class="flex gap-4">
        <button @click="handleDelete"
          class="text-xl hover:scale-110 hover:cursor-pointer transition ease-in-out duration-200"
        ><i class="pi pi-trash"></i></button>
        <button @click="handleActivity"
          class="text-xl hover:scale-110 hover:cursor-pointer transition ease-in-out duration-200"
        ><i v-if="account.isActive === 0" class="pi pi-eye"></i><i v-else class="pi pi-eye-slash"></i></button>
      </div>
    </span>
    <p class="text-xs text-neutral-400 mt-4">Spent this month</p>
    <span class="flex items-end justify-end h-10">
      <p class="text-2xl sm:text-4xl text-[#212529] font-bold">
        ${{ account.expenses.toFixed(2).split('.')[0] }}
      </p>
      <p class="text-md sm:text-xl text-[#212529] font-semibold">
        .{{ account.expenses.toFixed(2).split('.')[1] }}
      </p>
    </span>
  </div>
</template>