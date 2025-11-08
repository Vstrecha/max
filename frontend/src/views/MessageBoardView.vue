<script setup lang="ts">
import { open_tg_link } from '@/controllers/max'
import AvatarImage from '@/components/utility/AvatarImage.vue'

const test = () => {
  console.log('3')
  open_tg_link('https://t.me/?id=465954443')
}
</script>

<template>
  <section class="component-section-wrap">
    <h1>Message Board</h1>

    <h2 @click="test">will appear in next updates</h2>
    <a href="tg://user?id=465954443">ttt</a>
    <avatar-image width="170px" height="170px" signature="FF" />
  </section>
</template>

<style scoped>
h1 {
  margin: 60px 40px;
  font-size: 50px;
}
h2 {
  margin: 10px 40px;
  font-size: 30px;
}
</style>
