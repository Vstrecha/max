<script setup lang="ts">
import { ApiService } from '@/controllers/api'
import { notify } from '@/controllers/notifications'
import { VNotificationType } from '@/types/Notification'
import type { VProfile } from '@/types/Profile'
import { Overlay, Row, Button, Skeleton } from 'vant'
import { ref } from 'vue'
import ProfileCard from '../Profile/ProfileCard.vue'
import { haptic } from '@/controllers/max'
import { useUserStore } from '@/stores/userStore'

const props = defineProps<{
  invitation: string
}>()
const user_state = useUserStore()

const referrer = ref<VProfile | undefined>()
const show = ref(true)
const add_friend = () => {
  haptic.button_click()
  show.value = false
  ApiService.friends
    .add(props.invitation)
    .then(() => {
      notify(VNotificationType.SUCCESS, `Теперь вы друзья`)
    })
    .catch((error) => {
      notify(VNotificationType.ERROR, `Не смогли добавить в друзья. \n ${error}`)
      // :TODO: may be it is because user lose link to the bot
    })
}

function already_friends(profile_id: string) {
  return (
    user_state.profile?.id === profile_id ||
    user_state.friends?.some((friend) => friend.id === profile_id)
  )
}

function init() {
  ApiService.friends
    .check_invitation(props.invitation)
    .then((profile) => {
      if (!already_friends(profile.id)) referrer.value = profile
      else show.value = false
    })
    .catch((error) => notify(VNotificationType.ERROR, `Не смогли найти аккаунт друга. \n ${error}`))
}
init()
</script>

<template>
  <div class="request_wrap">
    <Overlay :show="show" @click="show = false">
      <div class="wrap">
        <div class="pop_up_wrap" @click.stop>
          <div class="pop_up_content">
            <h4 class="pop_up_text_title">Заявка в друзья</h4>
            <template v-if="referrer">
              <ProfileCard :profile="referrer" />
              <p class="pop_up_text">Ты перешёл по ссылке-приглашению. Добавить в друзья?</p>
            </template>
            <Skeleton v-else title round row="2"></Skeleton>
          </div>
          <Row justify="center">
            <Button @click="add_friend" text="Добавить" />
          </Row>
        </div>
      </div>
    </Overlay>
  </div>
</template>

<style scoped>
.wrap {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
}
.pop_up_wrap {
  width: 80%;
  box-sizing: border-box;
  background: var(--var-background-color);
  padding: 17px 20px;
  /* for the button */
  font-weight: 700;
  font-size: 14px;
}
.pop_up_content {
  margin-bottom: 11px;
}
.pop_up_text_title {
  text-align: center;
  font-weight: 700;
  font-size: 18px;
  color: var(--var-primary-emph-color);
}
.pop_up_text {
  font-weight: 500;
  font-size: 14px;
  color: var(--var-opposite-background-color);
}
</style>
