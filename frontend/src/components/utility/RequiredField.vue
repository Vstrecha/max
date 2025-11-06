<script setup lang="ts">
const {
  font_size = '14',
  keep_free_space = false,
  height = '18',
} = defineProps<{
  font_size?: string
  keep_free_space?: boolean
  height?: string
}>()
</script>

<template>
  <div
    class="required-field"
    :style="{
      'font-size': font_size + 'px',
      'margin-left': keep_free_space ? '5px' : 0,
      height: height + 'px',
    }"
  >
    *
  </div>
</template>

<style scoped>
.required-field {
  display: inline;
  color: var(--var-primary-emph-color);
}
</style>
