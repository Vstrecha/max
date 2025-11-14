<template>
  <Teleport to=".main-app-container">
    <div class="wrap">
      <Loading size="58" />
    </div>
  </Teleport>
</template>

<script setup lang="ts">
import { Loading } from 'vant'
</script>

<style scoped>
.wrap {
  position: fixed;
  left: 0;
  right: 0;
  top: 0;
  bottom: 0;
  display: flex;
  justify-content: center;
  align-items: center;
}
</style>
