<template>
  <Row>
    <Col span="4"></Col>
    <Col span="16">
      <div class="profile_name_wrap">
        <h2 class="profile_name">{{ get_header }}</h2>
      </div>
    </Col>
    <Col span="4">
      <div v-if="isEditable && !isCreating" class="control_buttons">
        <Settings v-if="!isEditing" :size="39" @click="start_editing" />
        <Check v-else :size="39" @click="save_changes" />
      </div>
    </Col>
  </Row>

  <Row justify="center">
    <div class="photo_wrapper">
      <AvatarImage
        width="170px"
        height="170px"
        :signature="get_name"
        :avatar_url="profile.avatar_url"
      />
      <div class="photo_edit" v-if="isEditing" @click="upload_photo">
        <Pencil :size="24" />
        <input
          type="file"
          ref="upload_photo_input"
          @change="on_photo_upload"
          accept="image/*"
          style="display: none"
        />
      </div>
    </div>
  </Row>
</template>

<script setup lang="ts">
import { ApiService } from '@/controllers/api'
import { haptic } from '@/controllers/max'
import type { VProfile } from '@/types/Profile'
import AvatarImage from '@/components/utility/AvatarImage.vue'
import { Col, Row } from 'vant'
import { Pencil, Settings, Check } from 'lucide-vue-next'
import { computed, useTemplateRef } from 'vue'
import { VFileType } from '@/types/Files'
import { notify } from '@/controllers/notifications'
import { VNotificationType } from '@/types/Notification'
import { useProfileActions } from '@/composables/useProfileActions'

const profile = defineModel<VProfile>({ required: true })
const states = defineProps<{
  isEditing?: boolean
  isEditable?: boolean
  isCreating?: boolean
}>()
const emit = defineEmits<{
  (e: 'start_editing'): void
  (e: 'save_changes'): void
}>()

const { get_name } = useProfileActions(profile)

const upload_photo_input = useTemplateRef('upload_photo_input')

const get_header = computed(() => {
  if (states.isCreating) return 'Новый профиль'
  else if (states.isEditing) return 'Редактирование'
  else return get_name
})


const upload_photo = function () {
  haptic.button_click()

  if (upload_photo_input.value) upload_photo_input.value.click()
}

const on_photo_upload = function (event: Event) {
  const target = event.target as HTMLInputElement
  const file = target.files?.[0]
  if (file) {
    ApiService.files
      .upload_file(file, VFileType.AVATAR)
      .then((uploaded_file) => {
        profile.value.avatar = uploaded_file.id
        profile.value.avatar_url = uploaded_file.url
      })
      .catch((error) => {
        console.log(error)
        notify(VNotificationType.ERROR, `Не смогли загрузить фотографию по причине: \n ${error}`)
      })
  }
}

const start_editing = function () {
  haptic.button_click()
  emit('start_editing')
}

const save_changes = function () {
  haptic.button_click()
  emit('save_changes')
}
</script>

<style scoped>
.profile_name_wrap {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
}
.profile_name {
  font-size: 20px;
  font-weight: 600;
  margin: 0 5px;
}
.control_buttons:hover {
  cursor: pointer;
}
.photo_wrapper {
  margin: 40px 0;
  width: 170px;
  height: 170px;
  position: relative;
}
.photo_edit {
  background: var(--var-small-parts-background-color);
  height: 48px;
  width: 48px;
  border-radius: 50%;
  border: 2px solid var(--var-secondary-emph-color);
  color: var(--var-secondary-emph-color);

  position: absolute;
  bottom: 0px;
  right: 0px;

  display: flex;
  align-items: center;
  justify-content: center;
}
.photo_edit:hover {
  cursor: pointer;
}
</style>
