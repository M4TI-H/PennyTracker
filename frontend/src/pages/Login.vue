<script setup>
import useScreenSize from '@/composables/screenSize';

const {screenWidth, screenHeight} = useScreenSize();
</script>

<template>
  <div class="fixed flex w-full h-full items-center justify-center gap-16 bg-[#DAD7CD] sm:py-16 ">
    <div class="w-[20%] h-96 flex flex-col items-center bg-[#E9ECEF] p-4 rounded-xl shadow-xl">
      <p class="text-2xl text-neutral-800 font-bold">Login</p>
      <span class="w-[90%] mt-8">
        <label>Name</label>
        <input type="text" class="w-full h-10 px-2 border-2 border-neutral-400 rounded-lg text-md font-medium
        focus:border-neutral-800 outline-0"/>
      </span>
      <span class="w-[90%] mt-8">
        <label>E-mail</label>
        <input type="text" class="w-full h-10 px-2 border-2 border-neutral-400 rounded-lg text-md font-medium
        focus:border-neutral-800 outline-0"/>
      </span>
      <button class="w-[50%] h-10 rounded-3xl mt-auto bg-neutral-800 text-sm text-[#E9ECEF]
        border-neutral-800 border-2 hover:cursor-pointer hover:bg-[#588157]
          transition ease-in-out duration-200 mb-1"
        >Login</button>
      </div>
  </div>
</template>