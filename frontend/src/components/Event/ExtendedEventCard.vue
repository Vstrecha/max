<script setup lang="ts">
import { useEventActions } from '@/composables/useEventActions'
import { type VExtendedEvent } from '@/types/Event'
import IconedTextField from '@/components/utility/IconedTextField.vue'

import { MapPin, CalendarClock, Users } from 'lucide-vue-next'
import { Button, Image as VanImage, Popup } from 'vant'
import { toRef } from 'vue'
import { haptic } from '@/controllers/max'

const props = defineProps<{
  extended_event: VExtendedEvent
}>()

const show_select_pop_up = defineModel<boolean>({ required: true })

const emit = defineEmits<{
  (e: 'select_event'): void
  (e: 'deselect_event'): void
  (e: 'edit_event'): void
}>()

const {
  get_participants,
  get_formatted_date,
  is_creator,
  is_viewer,
  get_tags,
  can_register,
  registrationBlockReason,
  open_qr,
} = useEventActions(toRef(props, 'extended_event'))

const select_event = () => {
  haptic.button_click()
  emit('select_event')
}

const deselect_event = () => {
  haptic.button_click()
  emit('deselect_event')
}

const edit_event = () => {
  haptic.button_click()
  emit('edit_event')
}
</script>

<template>
  <div class="extended-event-card">
    <div class="event_image_wrap">
      <VanImage width="100%" height="300px" fit="cover" :src="extended_event.event.photo_url" />
    </div>
    <div class="event_tags">{{ get_tags }}</div>

    <div class="event_body">
      <div class="event_info">
        <div class="event_info_part">
          <IconedTextField margin="8px 0" :text="extended_event.event.place || 'Неизвестно'">
            <MapPin :size="25" color="var(--var-secondary-emph-color)" />
          </IconedTextField>
          <IconedTextField margin="8px 0" :text="get_formatted_date">
            <CalendarClock :size="25" color="var(--var-secondary-emph-color)" />
          </IconedTextField>
          <IconedTextField margin="8px 0" :text="get_participants">
            <Users :size="25" color="var(--var-secondary-emph-color)" />
          </IconedTextField>
        </div>
      </div>

      <div class="event_description">
        {{ extended_event.event.body }}
      </div>
    </div>

    <div class="event_buttons">
      <div v-if="is_viewer">
        <Button
          @click="select_event"
          :text="can_register ? 'Хочу пойти!' : 'Регистрация недоступна'"
          :disabled="!can_register"
        />
        <p v-if="!can_register && registrationBlockReason" class="event_registration_hint">
          {{ registrationBlockReason }}
        </p>
      </div>

      <div v-else class="event_buttons_group">
        <div>
          <Button class="event_buttons_group_large" @click="open_qr" text="Открыть qr-код" />
        </div>
        <div>
          <Button
            v-if="is_creator"
            class="event_buttons_group_small"
            @click="edit_event"
            text="Изменить"
          />
          <Button
            v-else
            class="event_buttons_group_small"
            @click="deselect_event"
            text="Не смогу пойти"
          />
        </div>
      </div>
    </div>
    <Popup
      v-model:show="show_select_pop_up"
      round
      closeable
      position="bottom"
      :style="{ height: '30%' }"
    >
      <div class="pop_up_wrap">
        <div>
          <h4 class="pop_up_text_title">До встречи!</h4>
          <p class="pop_up_text">
            Успешно записали тебя. Список своих мероприятий ты всегда можешь найти на главной
            странице!
          </p>
        </div>
      </div>
    </Popup>
  </div>
</template>

<style scoped>
.extended-event-card {
  color: var(--var-opposite-background-color);
}

.extended-event-card .event_tags {
  font-weight: 300;
  font-size: 12px;
  color: var(--var-opposite-background-color);
}

.extended-event-card .event_body {
  margin: 20px 30px;
  font-weight: 400;
  font-size: 12px;
}

.extended-event-card .event_info {
  margin-bottom: 24px;
  display: flex;
  justify-content: space-between;
}
.extended-event-card .event_info_part:last-child {
  margin-left: 10px;
}
.extended-event-card .event_info_part {
  min-width: 35%;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.extended-event-card .event_description {
  font-weight: 400;
  font-size: 12px;
  line-height: 20px;
  white-space: pre-wrap;
}
.extended-event-card .event_buttons {
  margin: 30px;
  margin-bottom: 0;
  display: flex;
  justify-content: center;
  align-items: center;
  font-weight: 700;
  font-size: 14px;
  --van-button-normal-padding: 10px 80px;
}
.extended-event-card .event_buttons_group {
  width: 100%;
}
.extended-event-card .event_buttons_group_large {
  width: 100%;
  margin-bottom: 10px;
}
.extended-event-card .event_buttons_group_small {
  --van-button-normal-padding: 10px 10px;
  width: calc(50% - 5px);
}

.extended-event-card .pop_up_wrap {
  height: 100%;
  box-sizing: border-box;
  background: var(--var-background-color);
  padding: 17px 30px;
  /* for the button */
  font-weight: 700;
  font-size: 14px;
}

.extended-event-card .pop_up_text_title {
  text-align: center;
  font-weight: 700;
  font-size: 18px;
  color: var(--var-primary-emph-color);
}
.extended-event-card .pop_up_text {
  font-weight: 500;
  font-size: 14px;
  color: var(--var-opposite-background-color);
  margin-bottom: 27px;
}
.extended-event-card .event_registration_hint {
  margin-top: 10px;
  text-align: center;
  font-weight: 500;
  font-size: 12px;
  color: var(--var-opposite-background-color);
}
</style>
