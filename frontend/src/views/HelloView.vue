<script setup lang="ts">
import { notify } from '@/controllers/notifications'
import { useAppStore } from '@/stores/appStore'
import { VNotificationType } from '@/types/Notification'

import { Row, Button } from 'vant'
import { computed, ref, watch } from 'vue'

const app_state = useAppStore()

const show_share_btn = ref(false)
const texts = {
  new: {
    title: 'Добро пожаловать',
    body: '',
  },
  anonymous: {
    title: 'Не нашли ваш профиль',
    body: 'Чтобы создать аккаунт, нужно приглашение',
  },
}

const title_text = computed(() => texts[props.status].title)
const body_text = computed(() => texts[props.status].body)
const open_chat = () => {
  open_tg_link('https://t.me/stud_vstrecha_bot')
  app_state.endRegistrationMode()
}

function init() {
  if (props.status == 'new') {
    debugger
    create_bot_contact()
      .then(() => setTimeout(app_state.endRegistrationMode, 1500))
      .catch(() => {
        show_share_btn.value = true
        notify(VNotificationType.INFO, 'Нажмите на кнопку ниже, чтобы сохранить доступ к боту.')
      })
  }
}
init()
watch(() => props.status, init)
</script>

<template>
  <section class="component-section-wrap">
    <section class="component-section">
      <div class="content">
        <Row justify="center">
          <div class="logo_wrap">
            <img class="logo_icon" src="@/assets/icons/vstrecha-icon.svg" />
            <span class="logo_header">Встреча!</span>
          </div>
        </Row>
        <h1 class="headline">{{ title_text }}</h1>
        <h3 class="description">{{ body_text }}</h3>
        <Row justify="center">
          <div class="choose_new_event_button">
            <Button v-if="show_share_btn" @click="open_chat" text="Открыть бота" />
          </div>
        </Row>
      </div>
      <img class="background-effect-1" src="@/assets/icons/background-effect-hills.svg" />
      <img class="background-effect-2" src="@/assets/icons/background-effect-polylines.svg" />
    </section>
  </section>
</template>

<style scoped>
.component-section-wrap {
  position: relative;
}
.content {
  position: relative;
  z-index: 10;
}
.logo_wrap {
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

.headline {
  font-weight: 600;
  font-size: 24px;
  color: var(--var-secondary-emph-color);

  margin-top: 30vh;
  text-align: center;
}
.description {
  font-weight: 500;
  font-size: 11px;
  color: var(--var-opposite-background-color);

  margin: 32px 40px;

  text-align: center;
}

.background-effect-1 {
  position: absolute;
  top: 0;
  width: 100%;
  z-index: 0;
}
.background-effect-2 {
  position: absolute;
  bottom: 60px;
  width: 100%;
  z-index: 0;
}
</style>
