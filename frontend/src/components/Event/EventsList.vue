<script setup lang="ts">
import { onMounted, ref } from 'vue'

import EventCard from '@/components/Event/EventCard.vue'
import { type VExtendedEvent } from '@/types/Event'
import { List, PullRefresh } from 'vant'
import { notify } from '@/controllers/notifications'
import { VNotificationType } from '@/types/Notification'
import { useRoute } from 'vue-router'

const route = useRoute()
const props = defineProps<{
  events_list: VExtendedEvent[]
  load_more_events: () => Promise<void>
  reload_events: () => Promise<void>
  is_events_over: boolean
  is_loading_failed: boolean
}>()

const isRefreshing = ref(false)
const isLoading = ref(false)

const onLoad = async () => {
  try {
    await props.load_more_events()
    isLoading.value = false
  } catch (error) {
    notify(VNotificationType.ERROR, 'Не смогли загрузить новые встречи. ' + error)
  }
}

const onRefresh = async () => {
  try {
    await props.reload_events()
    isRefreshing.value = false
  } catch (error) {
    notify(VNotificationType.ERROR, 'Не смогли обновить список встреч. ' + error)
  }
}

function init() {
  const hash = route.hash.slice(1)
  const wrapper = document.querySelector('.component-section-wrap')
  if (hash !== '' && !isNaN(Number(hash)) && wrapper) {
    wrapper.scrollTop = Number(hash)
  } else if (props.events_list.length != 0) {
    props.reload_events()
  }
}
onMounted(init)
</script>

<template>
  <PullRefresh
    v-model="isRefreshing"
    @refresh="onRefresh"
    pulling-text="Потяните для обновления"
    loosing-text="Отпустите для обновления"
    loading-text="Обновляем"
  >
    <List
      v-model:loading="isLoading"
      :finished="is_events_over"
      :error="is_loading_failed"
      @load="onLoad"
      finished-text="Пока так"
      loading-text="Загружаем следующие встречи"
      error-text="Ошибка"
    >
      <div class="events_wrap">
        <EventCard
          v-for="event in events_list"
          :key="event.event.id"
          :data-id="event.event.id"
          :extended_event="event"
        />
      </div>
    </List>
  </PullRefresh>
</template>

<style>
.events_wrap {
  padding: 0 24px;
  width: 100%;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  align-items: center;
  /* overflow: auto; */
}
</style>
