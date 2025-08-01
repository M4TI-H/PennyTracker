import { ref, onMounted, onUnmounted } from "vue";
export default function useScreenSize() {

  const screenWidth = ref<number>(window.innerWidth);
  const screenHeight = ref<number>(window.innerHeight);

  const handleResize = () => {
    screenHeight.value = window.innerHeight;
    screenWidth.value = window.innerWidth;
  }

  onMounted(() => {
    window.addEventListener("resize", handleResize);
  });

  onUnmounted(() => {
    window.removeEventListener("resize", handleResize);
  });

  return {
    get screenWidth() {
      return screenWidth.value;
    },
    get screenHeight() {
      return screenHeight.value;
    }
  };
}