<script setup>
defineProps({
  screenWidth: Number,
})

const smallW = 640;
const mediumW = 768;

</script>

<template>
  <div 
      class="min-w-36 w-48 h-full flex flex-col items-center
      bg-[#588157] rounded-2xl shadow-xl"
      >
        <img src="https://plus.unsplash.com/premium_vector-1731582098134-9267458df79f?q=80&w=880&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
          class="size-16 self-center my-4"
        />
        <button class="w-full h-1/10 bg-none hover:bg-[#3A5A40]
          transition ease-in-out duration-200 hover:cursor-pointer
          text-sm font-semibold text-neutral-800"
        >
          <span class="flex items-center justify-center gap-2">
          <i class="pi pi-objects-column"></i>Dashboard
          </span>
        </button>
        <button class="w-full h-1/10 bg-none hover:bg-[#3A5A40]
          transition ease-in-out duration-200 hover:cursor-pointer
          text-sm font-semibold text-neutral-800"
        >
          <span class="flex items-center justify-center gap-2">
          <i class="pi pi-dollar"></i>Expenses
          </span>
        </button>
        <button class="w-full h-1/10 bg-none hover:bg-[#3A5A40]
          transition ease-in-out duration-200 hover:cursor-pointer
          text-sm font-semibold text-neutral-800"
        >
          <span class="flex items-center justify-center gap-2">
          <i class="pi pi-wallet"></i>Savings
          </span>
        </button>
        <button class="w-full h-1/10 bg-none hover:bg-[#3A5A40]
          transition ease-in-out duration-200 hover:cursor-pointer
          text-sm font-semibold text-neutral-800 mt-auto mb-8"
        >
          <span class="flex items-center justify-center gap-2">
          <i class="pi pi-sign-out"></i>Sign out
          </span>
        </button>
    </div>
</template>