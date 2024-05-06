<script setup>
import { useToast } from 'vue-toast-notification'
import { watch } from 'vue'
import Store from './utils/store.js'


const toast = useToast()
const store = Store()


watch(() => store.toast, (currentvalue, _) => {
  if (currentvalue.title == 'success') {
    toast.success(currentvalue.content);
  }
  else if (currentvalue.title == 'warning') {
    toast.warning(currentvalue.content);
  }
  else if (currentvalue.title == 'info') {
    toast.info(currentvalue.content);
  }
  else if (currentvalue.title == 'error') {
    toast.error(currentvalue.content);
  }
})

</script>

<template>
  <div class="main" @contextmenu.prevent>
    <router-view></router-view>
  </div>

  <div class="spin-custom" v-if="store.loading">
    <div class="spinner-border text-primary" role="status">
      <!-- <span class="sr-only">Loading...</span> -->
    </div>
  </div>

</template>

<style scoped>
.spin-custom {
  width: 100%;
  height: 100%;
  position: absolute;
  top: 0;
  left: 0;
  z-index: 100;
  display: grid;
  place-items: center;
}
</style>
