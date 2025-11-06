<script setup lang="ts">
import EventsList from '@/components/Event/EventsList.vue'
import { Funnel } from 'lucide-vue-next'
import { useGlobalEventsStore } from '@/stores/globalEventsStore'

const global_events = useGlobalEventsStore()
</script>

<template>
  <section class="events_main component-section-wrap">
    <section class="component-section">
      <div class="events_header">
        <h1 class="events_title">Выбрать Встречу!</h1>
        <Funnel :size="20" color="var(--var-secondary-emph-color)" />
      </div>
      <EventsList
        :events_list="global_events.events"
        :load_more_events="global_events.load_more_events"
        :reload_events="global_events.reload_events"
        :is_events_over="global_events.is_events_over"
        :is_loading_failed="global_events.is_failed"
      />
    </section>
  </section>
</template>

<style scoped>
.component-section {
  will-change: transform;
  transform: translateZ(0);
}
.events_header {
  padding: 24px;
  padding-top: 7px;
  display: flex;
  justify-content: space-between;
}
.events_title {
  margin: 0;
  font-weight: 600;
  font-size: 20px;
  color: var(--var-primary-emph-color);
}
</style>
