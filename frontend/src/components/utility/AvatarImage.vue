<script setup lang="ts">
import { Image as vanImage } from 'vant'
import { computed } from 'vue'

const props = defineProps<{
  width: string
  height: string
  avatar_url?: string
  signature?: string
  borderWeight?: string
  friend?: boolean
}>()
const color = computed(() =>
  props.friend ? 'var(--var-secondary-emph-color)' : 'var(--var-primary-emph-color)',
)

const border_style = computed(() => {
  return `${props.borderWeight ?? 3}px solid ${color.value}`
})

const font_size = computed(() => `${Number(props.borderWeight ?? 3) * 12}px`)
</script>

<template>
  <div class="avatar_wrap" :style="{ width: width, height: height, border: border_style }">
    <vanImage
      v-if="avatar_url"
      round
      fit="cover"
      :width="width"
      :height="height"
      :src="avatar_url"
    />
    <div
      v-else
      class="empty_avatar"
      :style="{ width: width, height: height, color: color, fontSize: font_size }"
    >
      <span>{{ signature ? signature[0] : '' }}</span>
    </div>
  </div>
</template>

<style scoped>
.avatar_wrap {
  display: inline-block;
  border-radius: 50%;
  background: var(--var-primary-emph-color);
}
.empty_avatar {
  border-radius: 50%;
  background: var(--var-small-parts-background-color);
  font-weight: 500;
  display: flex;
  justify-content: center;
  align-items: center;
}
</style>
