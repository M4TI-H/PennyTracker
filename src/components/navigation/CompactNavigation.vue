<script setup>
defineProps({
  screenWidth: Number,
})

const smallW = 640;

</script>

<template>
  <div class="fixed bottom-0 w-full h-12 flex bg-[#588157] z-10">
    <button class="w-1/4 h-full active:bg-[#3A5A40]"><i class="pi pi-objects-column"></i></button>
    <button class="w-1/4 h-full active:bg-[#3A5A40]"><i class="pi pi-dollar"></i></button>
    <button class="w-1/4 h-full active:bg-[#3A5A40]"><i class="pi pi-wallet"></i></button>
    <button class="w-1/4 h-full active:bg-[#3A5A40]"><i class="pi pi-sign-out"></i></button>
  </div>
</template>