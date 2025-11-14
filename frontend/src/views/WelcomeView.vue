<script setup lang="ts">
import AvatarImage from '@/components/utility/AvatarImage.vue'
import TextInput from '@/components/utility/TextInput.vue'
import { ApiService } from '@/controllers/api'
import { haptic, tg_state } from '@/controllers/max'
import { notify } from '@/controllers/notifications'
import { useAppStore } from '@/stores/appStore'
import { useUserStore } from '@/stores/userStore'
import { VNotificationType } from '@/types/Notification'
import { type VCreateProfile, VProfileSchema, VProfileSkeleton } from '@/types/Profile'
import { VFileType } from '@/types/Files'
import { Button, Row, Col } from 'vant'
import { ref } from 'vue'
import * as v from 'valibot'

const app_state = useAppStore()
const user_state = useUserStore()

const profileForm = ref(VProfileSkeleton())
if (tg_state.user_first_name)
  profileForm.value.first_name = tg_state.user_first_name
if (tg_state.user_last_name)
  profileForm.value.last_name = tg_state.user_last_name


const fileInput = ref<HTMLInputElement | null>(null)
const isUploadingAvatar = ref(false)
const isSubmitting = ref(false)

const openFilePicker = () => {
  haptic.button_click()
  fileInput.value?.click()
}

const onAvatarSelected = async (event: Event) => {
  const target = event.target as HTMLInputElement
  const file = target.files?.[0]
  if (!file) return

  isUploadingAvatar.value = true
  try {
    const uploaded = await ApiService.files.upload_file(file, VFileType.AVATAR)
    profileForm.value.avatar = uploaded.id
    profileForm.value.avatar_url = uploaded.url
  } catch (error) {
    notify(
      VNotificationType.ERROR,
      `Не удалось загрузить фотографию. Попробуй ещё раз. \n ${error}`,
    )
  } finally {
    isUploadingAvatar.value = false
    target.value = ''
  }
}

const validate_profile = (): boolean => {
  const validation = v.safeParse(VProfileSchema, profileForm.value)
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

const submitProfile = async () => {
  haptic.button_click()

  if (!validate_profile()) {
    return
  }

  const payload: VCreateProfile = {
    first_name: profileForm.value.first_name.trim(),
    last_name: profileForm.value.last_name.trim(),
    gender: profileForm.value.gender.trim(),
    birth_date: profileForm.value.birth_date,
    university: profileForm.value.university.trim(),
    avatar: profileForm.value.avatar
  }

  isSubmitting.value = true
  try {
    const created = await ApiService.profile.create_profile(payload)
    user_state.profile = created
    notify(VNotificationType.SUCCESS, `${created.first_name}, добро пожаловать!`)
    app_state.endRegistrationMode()
  } catch (error) {
    notify(VNotificationType.ERROR, `Не получилось создать профиль. \n ${error}`)
  } finally {
    isSubmitting.value = false
  }
}
</script>

<template>
  <section class="component-section-wrap">
    <section class="component-section">
      <img class="background-pattern" src="@/assets/icons/background-effect-lines.svg" />
      <div class="content">
        <Row justify="center">
          <div class="logo_wrap">
            <img class="logo_icon" src="@/assets/icons/max-events-icon.svg" />
            <span class="logo_header">Max!</span>
          </div>
        </Row>

        <div class="intro">
          <p class="product_description">
            На «Max!» студенты находят интересные события и собираются вместе офлайн.
            Подключайся, чтобы не пропускать тусовки своего университета и знакомиться с новыми
            людьми.
          </p>
        </div>

        <div class="form_wrap">
          <Row justify="center">
            <Col span="20">
            <div class="avatar_upload">
              <AvatarImage width="110px" height="110px" border-weight="2" :avatar_url="profileForm.avatar_url"
                :signature="profileForm.first_name ?? ''" />
              <Button round size="small" class="upload_button" :loading="isUploadingAvatar"
                :disabled="isUploadingAvatar" @click="openFilePicker">
                Загрузить фото
              </Button>
            </div>
            </Col>
          </Row>

          <TextInput class="info_field" title="Имя" v-model="profileForm.first_name" :editing="true" required />

          <TextInput class="info_field" title="Фамилия" v-model="profileForm.last_name" :editing="true" required />

          <TextInput class="info_field" title="Пол" v-model="profileForm.gender" :editing="true" input_type="gender"
            required />

          <TextInput class="info_field" title="Дата рождения" v-model="profileForm.birth_date" :editing="true"
            input_type="date" required />

          <TextInput class="info_field" title="ВУЗ" v-model="profileForm.university" :editing="true" required />

          <div class="submit_wrap">
            <Button type="primary" size="large" :loading="isSubmitting" @click="submitProfile">
              Зарегистрироваться
            </Button>
          </div>
        </div>
      </div>
    </section>
  </section>
  <input type="file" ref="fileInput" class="hidden_input" accept="image/*" @change="onAvatarSelected" />
</template>

<style scoped>
.component-section {
  position: relative;
}

.background-pattern {
  position: absolute;
  bottom: 40px;
  width: 100%;
  z-index: 0;
}

.content {
  position: relative;
  z-index: 10;
}

.logo_wrap {
  display: flex;
  justify-content: center;
  align-items: center;
}

.logo_icon {
  height: 24px;
  width: 24px;
  margin-right: 8px;
}

.logo_header {
  color: var(--var-opposite-background-color);
  font-weight: 700;
  font-size: 26px;
}

.intro {
  margin-top: 32px;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  gap: 24px;
}

.referrer {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
}

.referrer_name {
  color: var(--var-secondary-emph-color);
  font-size: 20px;
  font-weight: 600;
  margin: 0;
}

.referrer_caption {
  font-size: 13px;
  color: var(--var-opposite-background-color);
}

.product_description {
  font-size: 15px;
  line-height: 22px;
  color: var(--var-opposite-background-color);
  margin: 0 24px;
}

.form_wrap {
  margin-top: 36px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.avatar_upload {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
}

.upload_button {
  font-weight: 600;
}

.info_field {
  margin: 0 32px;
}

.submit_wrap {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
  margin: 0 32px;
}

.agreement_text {
  text-align: center;
  font-size: 11px;
  color: var(--var-opposite-background-color);
}

.agreement_link {
  color: var(--var-secondary-emph-color);
  text-decoration: underline;
}

.agreement_link:hover {
  cursor: pointer;
}

.hidden_input {
  display: none;
}
</style>
