<script setup lang="ts">
const { font_size = '11px' } = defineProps<{
  font_size?: string
  text: unknown
  margin?: string
}>()
</script>

<template>
  <div class="iconed-text-field" :style="{ margin }">
    <slot />
    <p class="text" :style="{ fontSize: font_size }">{{ text }}</p>
  </div>
</template>

<style scoped>
.iconed-text-field {
  display: flex;
  align-items: center;
}
.iconed-text-field .text {
  margin: 0;
  margin-left: 5px;
  color: var(--var-opposite-background-color);
  font-weight: 500;
}
</style>
