<script setup lang="ts">
import EventsList from '@/components/Event/EventsList.vue'
import { useUserEventsStore } from '@/stores/userEventsStore'
import { Row, Button } from 'vant'
import { useRoute, useRouter } from 'vue-router'
import { haptic } from '@/controllers/max'
import { computed, onMounted } from 'vue'
import { useUserStore } from '@/stores/userStore'

const user_events = useUserEventsStore()
const user_state = useUserStore()
const route = useRoute()
const router = useRouter()

const is_none_events = computed(() => user_events.is_events_over && user_events.events.length == 0)

// Загружаем события при первом рендере, если они еще не загружены
const loadEventsIfNeeded = () => {
  if (user_events.events.length === 0 && !user_events.is_events_over) {
    user_events.reload_events()
  }
}

onMounted(() => {
  loadEventsIfNeeded()
})

const is_moderator = computed(() => user_state.profile?.is_superuser === true)
// :TODO: ugly solution
const has_path_children = computed(() => route.name === 'friend_request')

const open_events_list = () => {
  haptic.button_click()
  router.push({ name: 'events' })
}

const open_create_event = () => {
  haptic.button_click()
  router.push({ name: 'create_event' })
}
</script>

<template>
  <section class="component-section-wrap home-view">
    <img class="background-effect" src="@/assets/icons/background-effect-corner-lines.svg" />
    <section class="component-section">
      <div class="header">
        <h2 class="title">Мои Встречи:</h2>
      </div>
      <EventsList
        v-if="!is_none_events"
        :events_list="user_events.events"
        :load_more_events="user_events.load_more_events"
        :reload_events="user_events.reload_events"
        :is_events_over="user_events.is_events_over"
        :is_loading_failed="user_events.is_failed"
      />
      <div v-else class="choose_new_event_wrap">
        <h3 class="choose_new_event_title">Пока пусто</h3>
        <p class="choose_new_event_text">
          Здесь появятся твои предстоящие встречи. Переходи в раздел “События”!
        </p>
        <Row justify="center">
          <div class="choose_new_event_button">
            <Button @click="open_events_list" type="primary" text="Выбрать встречу" />
          </div>
        </Row>
      </div>
    </section>

    <div v-if="is_moderator" class="create_event_block">
      <Button @click="open_create_event" type="primary">
        Создать событие
      </Button>
    </div>

    <div v-if="has_path_children">
      <router-view />
    </div>
  </section>
</template>

<style scoped>
.component-section-wrap {
  position: relative;
}
.component-section {
  position: relative;
}

.background-effect {
  position: fixed;
  top: 0;
  right: 0;
}
.header {
  padding: 24px;
  padding-top: 7px;
}
.title {
  margin: 0;
  font-weight: 600;
  font-size: 20px;
  color: var(--var-primary-emph-color);
}

.choose_new_event_wrap {
  margin: 20px 40px;
  padding: 37px 50px;

  background: var(--var-small-parts-background-color);
  color: var(--var-opposite-background-color);
  border-radius: 10px;
}
.choose_new_event_title {
  margin: 0;

  font-weight: 500;
  font-size: 18px;
  text-align: center;
}
.choose_new_event_text {
  margin: 0;
  margin-top: 20px;
  margin-bottom: 31px;
  font-weight: 500;
  font-size: 11px;
  text-align: center;
}
.choose_new_event_button {
  font-weight: 700;
  font-size: 14px;
}

.create_event_block {
  display: flex;
  justify-content: center;
  align-items: center;

  height: 12vh;
  width: 100%;

  background: #000000;
  background: linear-gradient(180deg, rgba(0, 0, 0, 0) 17%, rgba(26, 26, 26, 1) 100%);
  position: sticky;
  bottom: 0;
  padding-bottom: 26px;

  font-weight: 600;
  font-size: 14px;

  --van-button-normal-padding: 20px 90px;

  opacity: 0;
  animation: fadeIn 0.5s ease forwards;
  animation-delay: 0.3s;
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}
</style>
