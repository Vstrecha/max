<script setup lang="ts">
import AvatarImage from '@/components/utility/AvatarImage.vue'
import TextInput from '@/components/utility/TextInput.vue'
import { ApiService } from '@/controllers/api'
import { getLandingPreview, haptic } from '@/controllers/max'
import { notify } from '@/controllers/notifications'
import { useAppStore } from '@/stores/appStore'
import { useUserStore } from '@/stores/userStore'
import { VNotificationType } from '@/types/Notification'
import type { VProfile, VCreateProfile } from '@/types/Profile'
import { VFileType } from '@/types/Files'
import { Button, Row, Col } from 'vant'
import { computed, ref, watch } from 'vue'

const props = defineProps<{
  invitation?: string
}>()

const app_state = useAppStore()
const user_state = useUserStore()

const invitationCode = computed(() => props.invitation ?? '')
const referrer = ref<VProfile | undefined>()
const isReferrerLoading = ref(false)
const placeholderReferrer = getLandingPreview()

const profileForm = ref({
  name: '',
  birth_date: '',
  university: '',
  avatar: undefined as string | undefined,
  avatar_url: undefined as string | undefined,
})

const fileInput = ref<HTMLInputElement | null>(null)
const isUploadingAvatar = ref(false)
const isSubmitting = ref(false)

const canSubmit = computed(() => {
  return (
    invitationCode.value.trim().length > 0 &&
    profileForm.value.name.trim().length > 0 &&
    profileForm.value.birth_date.trim().length > 0 &&
    profileForm.value.university.trim().length > 0 &&
    !isSubmitting.value &&
    !isUploadingAvatar.value
  )
})

const displayName = computed(() => referrer.value?.name ?? placeholderReferrer.name)
const displayAvatar = computed(() => referrer.value?.avatar_url ?? placeholderReferrer.avatar_url)

watch(
  () => invitationCode.value,
  () => {
    if (!invitationCode.value) {
      referrer.value = undefined
      return
    }
    loadReferrer()
  },
  { immediate: true },
)

async function loadReferrer() {
  if (!invitationCode.value) return
  isReferrerLoading.value = true
  try {
    referrer.value = await ApiService.friends.check_invitation(invitationCode.value)
  } catch (error) {
    referrer.value = undefined
    notify(VNotificationType.ERROR, `Не получилось найти приглашение. \n ${error}`)
  } finally {
    isReferrerLoading.value = false
  }
}

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

const submitProfile = async () => {
  haptic.button_click()
  if (!invitationCode.value) {
    notify(VNotificationType.WARNING, 'Для регистрации нужна ссылка-приглашение.')
    return
  }
  if (!canSubmit.value) {
    notify(VNotificationType.WARNING, 'Заполни все поля, чтобы продолжить.')
    return
  }

  const payload: VCreateProfile = {
    name: profileForm.value.name.trim(),
    birth_date: profileForm.value.birth_date,
    university: profileForm.value.university.trim(),
    avatar: profileForm.value.avatar,
    invitation: invitationCode.value,
  }

  isSubmitting.value = true
  try {
    const created = await ApiService.profile.create_profile(payload)
    user_state.profile = created
    notify(VNotificationType.SUCCESS, `${created.name}, добро пожаловать!`)
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
            <img class="logo_icon" src="@/assets/icons/vstrecha-icon.svg" />
            <span class="logo_header">Встреча!</span>
          </div>
        </Row>

        <div class="intro">
          <div class="referrer" v-if="displayName">
            <AvatarImage
              width="120px"
              height="120px"
              border-weight="3"
              :avatar_url="displayAvatar"
              :signature="displayName"
            />
            <h2 class="referrer_name" v-if="!isReferrerLoading">{{ displayName }}</h2>
            <span class="referrer_caption" v-if="invitationCode">
              Уже во Встрече! и ждёт тебя
            </span>
          </div>

          <p class="product_description">
            На «Встречу!» студенты находят интересные события и собираются вместе офлайн.
            Подключайся, чтобы не пропускать тусовки своего университета и знакомиться с новыми
            людьми.
          </p>
        </div>

        <div class="form_wrap">
          <Row justify="center">
            <Col span="20">
              <div class="avatar_upload">
                <AvatarImage
                  width="110px"
                  height="110px"
                  border-weight="2"
                  :avatar_url="profileForm.avatar_url"
                  :signature="profileForm.name || 'Ты'"
                />
                <Button
                  round
                  size="small"
                  class="upload_button"
                  :loading="isUploadingAvatar"
                  :disabled="isUploadingAvatar"
                  @click="openFilePicker"
                >
                  Загрузить фото
                </Button>
              </div>
            </Col>
          </Row>

          <TextInput
            class="info_field"
            title="Имя и фамилия"
            v-model="profileForm.name"
            :editing="true"
            required
          />

          <TextInput
            class="info_field"
            title="Дата рождения"
            v-model="profileForm.birth_date"
            :editing="true"
            input_type="date"
            required
          />

          <TextInput
            class="info_field"
            title="ВУЗ"
            v-model="profileForm.university"
            :editing="true"
            required
          />

          <div class="submit_wrap">
            <Button
              type="primary"
              size="large"
              :loading="isSubmitting"
              :disabled="!canSubmit"
              @click="submitProfile"
            >
              Зарегистрироваться
            </Button>
          </div>
        </div>
      </div>
    </section>
  </section>
  <input
    type="file"
    ref="fileInput"
    class="hidden_input"
    accept="image/*"
    @change="onAvatarSelected"
  />
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
