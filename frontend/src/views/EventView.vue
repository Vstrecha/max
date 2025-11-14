<script setup lang="ts">
import {
  ParticipationType,
  VEventSchema,
  VExtendedEventSkeleton,
  type VEvent,
  type VExtendedEvent,
} from '@/types/Event'

import { Col, Row, Empty } from 'vant'
import * as v from 'valibot'
import { computed, ref, watch } from 'vue'
import { VNotificationType } from '@/types/Notification'
import { notify } from '@/controllers/notifications'
import { useAppStore } from '@/stores/appStore'
import ExtendedEventCard from '@/components/Event/ExtendedEventCard.vue'
import EditingEventCard from '@/components/Event/EditingEventCard.vue'
import { ApiService } from '@/controllers/api'
import { getRegistrationState, normalizeDateTimeForApi } from '@/utils/eventRegistration'

const app_state = useAppStore()
const props = defineProps<{
  event_id: string
}>()
const event = ref<VExtendedEvent | undefined>()

const sanitizeEvent = (target: VEvent) : VEvent => {
  target.registration_start_date = normalizeDateTimeForApi(target.registration_start_date)
  target.registration_end_date = normalizeDateTimeForApi(target.registration_end_date)
  target.is_registration_available = getRegistrationState(target).isAvailable

  return target
}

function init() {
  isCreating.value = false
  isEditing.value = false

  if (props.event_id == 'new') {
    isCreating.value = true
    isEditing.value = true
    event.value = VExtendedEventSkeleton()
  } else if (props.event_id === app_state.activeEventCard?.event.id) {
    event.value = app_state.activeEventCard
  } else {
    event.value = undefined
    notify(VNotificationType.ERROR, `Задан неверный id события. \n id: ${props.event_id}`)
  }
}

const isEditing = ref(false)
const isCreating = ref(false)
const is_event_processed = ref(false)
const show_select_pop_up = ref(false)

const get_header = computed(() => {
  if (isCreating.value) return 'Новое событие'
  else if (isEditing.value) return 'Редактирование'
  else return event.value?.event.title
})

const start_editing = () => {
  isEditing.value = true
}
const cancel_editing = () => {
  isEditing.value = false
}

const select_event = () => {
  if (!event.value) return
  const registrationState = getRegistrationState(event.value.event)
  const reason = registrationState.reason
  if (reason) {
    notify(VNotificationType.WARNING, reason)
    return
  }

  ApiService.events
    .select_event(event.value.event.id)
    .then(() => {
      show_select_pop_up.value = true
      if (!event.value) return
      // :TODO: Is it the best solution?
      event.value.participation_type = ParticipationType.PARTICIPANT
      event.value.event.participants += 1
      const updatedState = getRegistrationState(event.value.event)
      event.value.event.is_registration_available = updatedState.isAvailable
    })
    .catch((error) => notify(VNotificationType.ERROR, `Не смогли добавить. \n ${error}`))
}
const deselect_event = () => {
  if (!event.value) return

  ApiService.events
    .deselect_event(event.value.event.id)
    .then(() => {
      notify(VNotificationType.SUCCESS, 'Отменили ваше участие. Предупредите об этом организатора')
      if (!event.value) return
      // :TODO: Is it the best solution?
      event.value.participation_type = ParticipationType.VIEWER
      event.value.event.participants = Math.max(0, event.value.event.participants - 1)
      const updatedState = getRegistrationState(event.value.event)
      event.value.event.is_registration_available = updatedState.isAvailable
    })
    .catch((error) => notify(VNotificationType.ERROR, `Не смогли отменить. \n ${error}`))
}

const process_event = async (new_event: VEvent) => {
  const sanitized_event = sanitizeEvent(new_event)
  if (!validate_event(sanitized_event)) return

  is_event_processed.value = true

  if (isCreating.value) {
    await create_event(sanitized_event)
  } else {
    await update_event(sanitized_event)
  }
  isEditing.value = false
  isCreating.value = false
  is_event_processed.value = false
}

const validate_event = (new_event: VEvent) => {
  const validation = v.safeParse(VEventSchema, new_event)
  if (!validation.success) {
    let error_message = ''
    validation.issues.forEach((error) => {
      error_message += error.message + '\n'
    })
    notify(VNotificationType.WARNING, `Неккоректно заполнены поля: \n ${error_message}`)
    return false
  }
  return true
}

const create_event = async (new_event: VEvent) => {
  try {
    const created_event = await ApiService.events.create_event(new_event)
    notify(VNotificationType.SUCCESS, 'Событие создано!')
    // :TODO: Is it the best idea?
    app_state.openExtendedEventCard({
      event: { ...created_event },
      friends_going: 0,
      participation_type: ParticipationType.CREATOR,
    })
  } catch (error) {
    notify(VNotificationType.ERROR, `Не смогли создать событие. \n ${error}`)
  }
}

const update_event = async (new_event: VEvent) => {
  try {
    const updated_event = await ApiService.events.edit_event(new_event)
    notify(VNotificationType.SUCCESS, 'Сохранили изменения!')
    if (event.value) event.value.event = updated_event
  } catch (error) {
    notify(VNotificationType.ERROR, `Не смогли обновить событие. \n ${error}`)
  }
}

init()
watch(() => props.event_id, init)
</script>

<template>
  <section class="component-section-wrap event-view">
    <section class="component-section">
      <template v-if="event != undefined">
        <header>
          <Row>
            <Col span="2"></Col>
            <Col span="20">
              <h2 class="title">{{ get_header }}</h2>
            </Col>
            <Col span="2"> </Col>
          </Row>
        </header>

        <EditingEventCard
          v-if="isEditing"
          :extended_event="event"
          :is-creating="isCreating"
          :is_button_loading="is_event_processed"
          @cancel="cancel_editing"
          @update_event="process_event"
        />
        <ExtendedEventCard
          v-else
          :extended_event="event"
          v-model="show_select_pop_up"
          @select_event="select_event"
          @deselect_event="deselect_event"
          @edit_event="start_editing"
        />
      </template>
      <Empty v-else image="error" description="Не смогли найти выбранное событие" />
    </section>
  </section>
</template>

<style scoped>
.event-view .edit-event {
  /* background-color: red; */
  margin: 0 34px;
}
.event-view .upload_photo_wrap {
  width: 100%;
  margin-bottom: 23px;

  display: flex;
  justify-content: center;
  align-items: center;
}
</style>
