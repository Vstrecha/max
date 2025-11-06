<script setup lang="ts">
import { ApiService } from '@/controllers/api'
import { notify } from '@/controllers/notifications'
import { VNotificationType } from '@/types/Notification'
import type { VProfile } from '@/types/Profile'

import { Row, Col, Button, Image as vanImage } from 'vant'
import { computed, ref } from 'vue'
import CentralLoader from '@/components/utility/CentralLoader.vue'
import { useAppStore } from '@/stores/appStore'
import { haptic } from '@/controllers/max'

const props = defineProps<{
  invitation: string
}>()
const referrer = ref(undefined as VProfile | undefined)
const isLoading = ref(true)
const app_state = useAppStore()

ApiService.friends
  .check_invitation(props.invitation)
  .then((referrer_loaded) => {
    referrer.value = referrer_loaded
    isLoading.value = false
  })
  .catch((error) => {
    isLoading.value = false
    notify(VNotificationType.ERROR, error)
  })

const get_referrer_name = computed(() =>
  referrer.value != undefined
    ? referrer.value.first_name + ' ' + referrer.value.last_name
    : 'Ищем, кто же...',
)

const start_registration = () => {
  haptic.button_click()
  app_state.openRegistrationMode(props.invitation)
}

const open_official = () => {
  haptic.button_click()
  app_state.open_official()
}
</script>

<template>
  <section class="component-section-wrap">
    <section class="component-section">
      <img class="component-background-1" src="@/assets/icons/background-effect-1.svg" />
      <img class="component-background-lines" src="@/assets/icons/background-effect-lines.svg" />

      <div class="background_effects_content">
        <Row justify="center">
          <Col span="20">
            <div class="logo_wrap">
              <img class="logo_icon" src="@/assets/icons/vstrecha-icon.svg" />
              <span class="logo_header">Встреча!</span>
            </div>
          </Col>
        </Row>

        <template v-if="!isLoading && referrer != undefined">
          <div class="referrer">
            <div class="referrer_photo">
              <vanImage
                round
                fit="cover"
                width="170px"
                height="170px"
                :src="referrer?.avatar_url ?? ''"
              />
            </div>
            <h2 class="referrer_name">
              {{ get_referrer_name }}
            </h2>
          </div>

          <div class="content">
            <p class="invitation_text">
              Приглашает тебя стать частью <br /><span class="invitation_text_empth">Встречи!</span>
            </p>
            <div class="quote_text">
              <p>Тут студенты разных вузов находят интересные события и собираются вместе!</p>
            </div>
          </div>

          <Row justify="center">
            <div class="create_button_wrap">
              <Button type="primary" @click="start_registration">Зарегистрироваться</Button>
              <span class="create_button_description">
                Продолжая, вы даёте согласение на обработку персональных данных и соглашаетесь с
                <span
                  class="create_button_description_link"
                  href="/official"
                  @click.stop="open_official"
                >
                  публичной офертой
                </span>
              </span>
            </div>
          </Row>
        </template>
        <CentralLoader v-else-if="isLoading" />
        <template v-else>
          <!-- invalid invitation -->
          <h2 class="invalid_invitation_text">
            Не можем найти, кто же тебя пригласил. Попроси ещё раз прислать приглашение.
          </h2>
        </template>
      </div>
    </section>
  </section>
</template>

<style scoped>
.component-section-wrap {
  position: relative;
}

.component-section .component-background-1 {
  position: absolute;
  top: 0;
  right: 0;
  z-index: 0;
}

.component-section .component-background-lines {
  position: absolute;
  width: 100%;
  left: 0;
  right: 0;
  bottom: 80px;
  z-index: 0;
}

.component-section .background_effects_content {
  position: relative;
  z-index: 2;
}

.component-section .logo_wrap {
  display: flex;
  justify-content: center;
  align-items: center;

  z-index: 10;
}
.logo_icon {
  height: 25px;
  width: 25px;

  padding-top: 5px;
  margin-right: 8px;
}
.logo_header {
  color: var(--var-opposite-background-color);
  font-weight: 700;
  font-size: 28px;
}

.referrer {
  margin-top: 60px;
  display: flex;
  flex-direction: column;
  align-items: center;
}
.referrer_photo {
  width: 170px;
  height: 170px;
  display: inline-block;
  position: relative;

  border-radius: 50%;
  border: 3px solid var(--var-primary-emph-color);
  background: var(--var-primary-emph-color);
}
.referrer_name {
  margin: 0;
  margin-top: 20px;
  text-align: center;

  font-weight: 600;
  font-size: 19px;
  color: var(--var-secondary-emph-color);
}
.content {
  margin: 36px 28px;
  font-weight: 700;
  font-size: 20px;

  color: var(--var-opposite-background-color);
}

.invitation_text {
  line-height: 25px;
  text-align: center;
}

.quote_text {
  margin-top: 34px;
  font-weight: 400;
  font-size: 12px;

  text-align: end;
}

.create_button_wrap {
  margin-top: 120px;
  width: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;

  font-weight: 700;
  font-size: 16px;
}

.create_button_description {
  width: 80%;
  margin-top: 7px;
  text-align: center;

  font-weight: 300;
  font-size: 9px;

  color: var(--var-opposite-background-color);
}
.create_button_description_link {
  color: var(--var-secondary-emph-color);
  text-decoration: underline;
}
.invalid_invitation_text {
  margin-top: 84px;
  color: var(--var-opposite-background-color);
}
</style>
