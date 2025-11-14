<script setup lang="ts">
import {
  type VEvent,
  type VExtendedEvent,
} from '@/types/Event'
import { ApiService } from '@/controllers/api'
import { VFileType } from '@/types/Files'
import { ALL_TAGS } from '@/stores/userStore'
import { notify } from '@/controllers/notifications'
import { VNotificationType } from '@/types/Notification'
import { haptic } from '@/controllers/max'
import RequiredField from '@/components/utility/RequiredField.vue'

import { ref, toRaw, useTemplateRef, watch } from 'vue'
import { MapPin, CalendarClock, Pencil, Users } from 'lucide-vue-next'
import { Button, Image as VanImage, Field, CellGroup } from 'vant'

const props = defineProps<{
  extended_event: VExtendedEvent
  isCreating?: boolean
  is_button_loading: boolean
}>()

const emit = defineEmits<{
  (e: 'cancel'): void
  (e: 'update_event', new_event: VEvent): void
}>()
type NormalizableEvent = VEvent & {
  registration_start_date?: string
  registration_end_date?: string
}

const pad = (value: number): string => value.toString().padStart(2, '0')

const toDateTimeLocal = (value: string | undefined): string | undefined => {
  if (!value) return undefined
  const date = new Date(value)
  if (Number.isNaN(date.getTime())) {
    return value.slice(0, 16)
  }
  return `${date.getFullYear()}-${pad(date.getMonth() + 1)}-${pad(date.getDate())}T${pad(date.getHours())}:${pad(date.getMinutes())}`
}

const normalizedEvent = (): NormalizableEvent => {
  const cloned = structuredClone(toRaw(props.extended_event.event)) as NormalizableEvent
  cloned.registration_start_date = toDateTimeLocal(cloned.registration_start_date)
  cloned.registration_end_date = toDateTimeLocal(cloned.registration_end_date)
  return cloned
}

const event = ref<NormalizableEvent>(normalizedEvent())

watch(
  () => event.value.registration_start_date,
  (value) => {
    if (!value || value === '') {
      event.value.registration_start_date = undefined
    }
  },
)

watch(
  () => event.value.registration_end_date,
  (value) => {
    if (!value || value === '') {
      event.value.registration_end_date = undefined
      return
    }
    if (event.value.registration_start_date) {
      const start = new Date(event.value.registration_start_date)
      const end = new Date(value)
      if (!Number.isNaN(start.getTime()) && !Number.isNaN(end.getTime()) && end < start) {
        event.value.registration_start_date = value
      }
    }
  },
)

watch(
  () => props.extended_event,
  () => {
    event.value = normalizedEvent()
  },
)

watch(
  () => event.value.max_participants,
  (value) => {
    if (value === null || Number.isNaN(value as number)) {
      event.value.max_participants = undefined
    } else if (typeof value === 'number' && value < 1) {
      event.value.max_participants = 1
    }
  },
)

const upload_photo_input = useTemplateRef('upload_photo_input')


const select_tag = (tag: string) => {
  haptic.button_click()
  const tags = event.value.tags
  if (event.value.tags.includes(tag)) {
    tags.splice(
      tags.findIndex((el) => el === tag),
      1,
    )
  } else {
    tags.push(tag)
  }
}

const upload_photo = () => {
  haptic.button_click()

  if (upload_photo_input.value) upload_photo_input.value.click()
}

const on_photo_upload = function (upload_event: Event) {
  const target = upload_event.target as HTMLInputElement
  const file = target.files?.[0]
  if (file) {
    ApiService.files
      .upload_file(file, VFileType.EVENT)
      .then((uploaded_file) => {
        event.value.photo_url = uploaded_file.url
        event.value.photo = uploaded_file.id
      })
      .catch((error) => {
        console.log(error)
        notify(VNotificationType.ERROR, `Не смогли загрузить фотографию по причине: \n ${error}`)
      })
  }
}

const cancel = () => {
  haptic.button_click()
  emit('cancel')
}

const update_event = async () => {
  haptic.button_click()
  emit('update_event', event.value)
}
</script>

<template>
  <div class="editing-event-card">
    <div class="upload_photo_wrap">
      <div class="upload_photo" @click="upload_photo">
        <template v-if="event.photo_url">
          <vanImage fit="cover" width="130px" height="130px" :src="event.photo_url" />
          <div class="upload_photo_edit_button_wrap">
            <div class="upload_photo_button upload_photo_edit_button">
              <Pencil :size="18" color="var(--var-secondary-emph-color)" />
            </div>
          </div>
        </template>
        <template v-else>
          <img
            v-if="!event.photo_url"
            class="upload_photo_button"
            src="@/assets/icons/add-photo-button.svg"
            alt="Добавить фото"
          />
        </template>

        <input
          type="file"
          ref="upload_photo_input"
          @change="on_photo_upload"
          accept="image/*"
          style="display: none"
        />
      </div>
    </div>

    <div class="edit-information">
      <div class="info_group">
        <h4 class="info_group_title">Название <RequiredField font_size="18" /></h4>
        <div class="info_border_wrap">
          <div class="input_field_wrap">
            <CellGroup inset>
              <Field
                v-model="event.title"
                type="textarea"
                placeholder="Давайте встретимся и ..."
                rows="1"
                autosize
              />
            </CellGroup>
          </div>
        </div>
      </div>

      <div class="info_group">
        <div class="info_border_wrap">
          <div class="info_field_flex">
            <MapPin :size="18" color="var(--var-secondary-emph-color)" />
            <div class="input_field_wrap info_field_input">
              <CellGroup inset>
                <Field
                  v-model="event.place"
                  type="textarea"
                  placeholder="Укажите место"
                  rows="1"
                  autosize
                />
              </CellGroup>
            </div>
          </div>
        </div>
      </div>

      <div class="info_group">
        <h4 class="info_group_title">Количество участников</h4>
        <div class="info_border_wrap">
          <div class="info_field_flex">
            <Users :size="18" color="var(--var-secondary-emph-color)" />
            <div class="input_field_wrap info_field_input">
              <CellGroup inset>
                <Field
                  v-model.number="event.max_participants"
                  type="digit"
                  placeholder="Без ограничения"
                  :formatter="(value: string) => value.replace(/[^0-9]/g, '')"
                />
              </CellGroup>
            </div>
          </div>
        </div>
      </div>

      <div class="info_group">
        <h4 class="info_group_title">Время мероприятия</h4>
        <div class="info_border_wrap">
          <div class="edit_date_group">
            <CalendarClock :size="20" color="var(--var-secondary-emph-color)" />
            <RequiredField font_size="18" keep_free_space height="32" />
            <img class="edit_date_group_separator" src="@/assets/icons/edit_event_date.svg" />
            <div class="edit_date_group_data_picker_wrap">
              <div class="edit_date_group_data_picker">
                <span>Начало</span>
                <input type="date" v-model="event.start_date" />
              </div>
              <div class="edit_date_group_data_picker_line"></div>
              <div class="edit_date_group_data_picker">
                <span>Конец</span>
                <input type="date" v-model="event.end_date" />
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="info_group">
        <h4 class="info_group_title">Время регистрации</h4>
        <div class="info_border_wrap">
          <div class="edit_date_group">
            <CalendarClock :size="20" color="var(--var-secondary-emph-color)" />
            <div class="edit_date_group_data_picker_wrap">
              <div class="edit_date_group_data_picker">
                <span>Открытие</span>
                <input
                  type="datetime-local"
                  v-model="event.registration_start_date"
                  :max="event.registration_end_date"
                />
              </div>
              <div class="edit_date_group_data_picker_line"></div>
              <div class="edit_date_group_data_picker">
                <span>Закрытие</span>
                <input
                  type="datetime-local"
                  v-model="event.registration_end_date"
                  :min="event.registration_start_date"
                />
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="info_group">
        <h4 class="info_group_title">Описание <RequiredField font_size="18" /></h4>
        <div class="info_border_wrap">
          <div class="input_field_wrap">
            <CellGroup inset>
              <Field
                v-model="event.body"
                type="textarea"
                placeholder="Мы будем ..."
                rows="4"
                autosize
              />
            </CellGroup>
          </div>
        </div>
      </div>

      <div class="info_group">
        <h4 class="info_group_title">Выберите теги:</h4>
        <div class="tags_wrap">
          <span
            class="tag"
            :class="{ tag_active: event.tags.includes(tag) }"
            @click="() => select_tag(tag)"
            v-for="tag in ALL_TAGS"
            :key="tag"
            >#{{ tag }}</span
          >
        </div>
      </div>
    </div>
    <div class="update_button">
      <Button v-if="isCreating" text="Создать" :loading="is_button_loading" @click="update_event" />
      <div v-else>
        <Button text="Отменить" @click="cancel" />
        <div style="width: 10px; display: inline-block"></div>
        <Button text="Сохранить" :loading="is_button_loading" @click="update_event" />
      </div>
    </div>
  </div>
</template>

<style scoped>
.editing-event-card {
  margin: 0 24px;
}

/* PHOTO */
.editing-event-card .upload_photo_wrap {
  width: 100%;
  margin-bottom: 23px;

  display: flex;
  justify-content: center;
  align-items: center;

  position: relative;
}
.editing-event-card .upload_photo {
  width: 130px;
  height: 130px;
  display: flex;
  justify-content: center;
  align-items: center;
  overflow: hidden;

  background: var(--var-small-parts-background-color);
  border-radius: 20px;
}
.editing-event-card .upload_photo:hover {
  cursor: pointer;
}

.editing-event-card .upload_photo_button {
  position: absolute;
}

.editing-event-card .upload_photo_edit_button_wrap {
  position: absolute;
  width: 130px;
  height: 130px;
}

.editing-event-card .upload_photo_edit_button {
  background: var(--var-small-parts-background-color);
  height: 48px;
  width: 48px;
  border-radius: 50%;
  border: 2px solid var(--var-secondary-emph-color);
  color: var(--var-secondary-emph-color);

  position: absolute;
  bottom: -12px;
  right: -12px;

  display: flex;
  align-items: center;
  justify-content: center;
}
/* INFORAMTION */
.editing-event-card .info_border_wrap {
  border: 1px solid var(--var-primary-emph-color);
  border-radius: 10px;

  padding: 8px 9px;
}
.editing-event-card .info_group {
  margin-bottom: 16px;
}

.editing-event-card .info_group_title {
  font-weight: 500;
  font-size: 18px;
  margin: 0;
  margin-bottom: 11px;
  color: var(--var-secondary-emph-color);
}

.info_group_hint {
  font-weight: 400;
  font-size: 10px;
  margin: 0;

  color: var(--var-opposite-background-color);
}

/* DATE */
.editing-event-card .edit_date_group {
  display: flex;
  align-items: center;
}
.editing-event-card .edit_date_group_separator {
  margin-left: 8px;
  margin-right: 4px;

  height: 45px;
}

.editing-event-card .edit_date_group_data_picker_wrap {
  flex-grow: 1;
  display: flex;
  flex-direction: column;

  margin-left: 10px;
}

.editing-event-card .edit_date_group_data_picker {
  display: flex;
  align-items: center;
  justify-content: space-between;

  font-weight: 400;
  font-size: 12px;
}

.editing-event-card .edit_date_group_data_picker span {
  margin-left: 6px;
  color: var(--var-opposite-background-color);
}

.editing-event-card .edit_date_group_data_picker input {
  color: var(--var-opposite-background-color);
  background: var(--var-primary-emph-color);
  border: none;
  border-radius: 5px;
}


.editing-event-card .registration_group input {
  width: 100%;
  color: var(--var-opposite-background-color);
  background: var(--var-primary-emph-color);
  border: none;
  border-radius: 5px;
  padding: 4px 6px;
}

.editing-event-card .edit_date_group_data_picker_line {
  margin: 5px 0;
  background-color: var(--var-primary-emph-color);
  height: 1px;
  width: 100%;
}

/* FIELDS */
.editing-event-card .info_field_flex {
  display: flex;
  justify-content: center;
  align-items: center;
}

.editing-event-card .info_field_input {
  flex-grow: 1;
  margin-left: 7px;
}

/* TOGGLE */
.editing-event-card .toggle_option_text_wrap {
  flex-grow: 1;
  margin-left: 8px;
  margin-right: 18px;

  display: flex;
  flex-direction: column;
  align-items: start;
}

.editing-event-card .toggle_option_text_title {
  font-weight: 400;
  font-size: 12px;
  color: var(--var-secondary-emph-color);
}

.editing-event-card .toggle_option_text_description {
  margin-top: 5px;
  font-weight: 400;
  font-size: 10px;
  color: var(--var-opposite-background-color);
}
/* DESCRIPTION */
.editing-event-card .input_field_wrap {
  color: var(--var-opposite-background-color);
  --van-cell-group-inset-padding: 0;
  --van-cell-background: var(--var-background-color);
  --van-field-input-text-color: var(--var-opposite-background-color);
  --van-cell-group-background: transparent;
  --van-cell-vertical-padding: 0;
  --van-cell-horizontal-padding: 0;
}

/* TAGS */
.editing-event-card .tag {
  font-weight: 400;
  font-size: 12px;
  color: var(--var-opposite-background-color);

  display: inline-block;
  padding: 4px 10px;
  margin-right: 9px;
  margin-bottom: 9px;

  border: 1px solid var(--var-primary-emph-color);
  border-radius: 10px;

  transition-duration: 0.2s;
}
.editing-event-card .tag:hover {
  cursor: pointer;
}

.editing-event-card .tag_active {
  background: var(--var-secondary-emph-color);
  color: var(--var-background-color);
  border: 1px solid var(--var-secondary-emph-color);
}

/* BUTTON */

.editing-event-card .update_button {
  padding-top: 15px;
  display: flex;
  justify-content: center;
  align-items: center;

  --van-button-default-color: var(--var-secondary-emph-color);
  font-weight: 700;
  font-size: 14px;
}
</style>
