<script setup lang="ts">
import useScreenSize from '@/composables/screenSize';

const { screenWidth, screenHeight } = useScreenSize();

const smallW = 640;
const mediumW = 768;
</script>

<template>
  <div class="min-w-36 w-48 h-full flex flex-col items-center
    bg-[#588157] rounded-2xl shadow-xl"
  >
    <img src="https://plus.unsplash.com/premium_vector-1731582098134-9267458df79f?q=80&w=880&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
      class="size-16 self-center my-4"
    />
    <RouterLink tag="button" to="/" class="w-full h-1/10 bg-none hover:bg-[#3A5A40]
      transition ease-in-out duration-200 hover:cursor-pointer
      text-sm font-semibold text-neutral-800 flex items-center justify-center gap-2"
    >
      <span class="w-[50%] flex justify-between items-center">
      <i class="pi pi-objects-column"></i>Dashboard
      </span>
    </RouterLink>
    <RouterLink tag="button" to="/expenses" class="w-full h-1/10 bg-none hover:bg-[#3A5A40]
      transition ease-in-out duration-200 hover:cursor-pointer
      text-sm font-semibold text-neutral-800 flex items-center justify-center gap-2"
    >
      <span class="w-[50%] flex justify-between items-center">
      <i class="pi pi-dollar"></i>Expenses
      </span>
    </RouterLink>
    <RouterLink tag="button" to="/savings" class="w-full h-1/10 bg-none hover:bg-[#3A5A40]
      transition ease-in-out duration-200 hover:cursor-pointer
      text-sm font-semibold text-neutral-800 flex items-center justify-center gap-2"
    >
    <span class="w-[50%] flex justify-between items-center">
      <i class="pi pi-wallet"></i>Savings
    </span>
    </RouterLink>
    <RouterLink tag="button" to="/options" class="w-full h-1/10 bg-none hover:bg-[#3A5A40]
      transition ease-in-out duration-200 hover:cursor-pointer
      text-sm font-semibold text-neutral-800 flex justify-center gap-2"
    >
      <span class="w-[50%] flex justify-between items-center">
        <i class="pi pi-cog"></i>Options
      </span>
    </RouterLink>
    <RouterLink tag="button" to="/login" class="w-full h-1/10 bg-none hover:bg-[#3A5A40]
      transition ease-in-out duration-200 hover:cursor-pointer
      text-sm font-semibold text-neutral-800 mt-auto mb-8 flex items-center justify-center gap-2"
    >
      <span class="w-[50%] flex justify-between items-center">
      <i class="pi pi-sign-out"></i>Sign out
      </span>
    </RouterLink>
  </div>
</template>