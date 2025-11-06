<script setup lang="ts">
import { ApiService } from '@/controllers/api'
import { notify } from '@/controllers/notifications'
import { VNotificationType } from '@/types/Notification'
import type { VProfile } from '@/types/Profile'
import { ref, watch } from 'vue'
import ProfileCard from '@/components/Profile/ProfileCard.vue'
import { useAppStore } from '@/stores/appStore'

const props = defineProps<{
  profile_id: string
}>()
const app_state = useAppStore()

const friends = ref<VProfile[] | undefined>()
const open_profile = (profile_id: string) => {
  app_state.openProfilePage(profile_id)
}

function init() {
  ApiService.friends
    .get(props.profile_id)
    .then((loaded_friends) => {
      friends.value = loaded_friends.reverse()
    })
    .catch((error) =>
      notify(VNotificationType.ERROR, `Не смогли загрузить список друзей. \n ${error}`),
    )
}
init()
watch(() => props.profile_id, init)
</script>

<template>
  <section class="component-section-wrap">
    <section class="component-section">
      <h2 class="title">Друзья</h2>
      <!-- <p class="description">
        Чтобы пригласить друга, нажмите <span class="emph" @click="invite">сюда</span>
      </p> -->
      <div class="profiles_wrap">
        <div
          class="friend_card"
          v-for="friend in friends"
          :key="friend.id"
          @click="() => open_profile(friend.id)"
        >
          <ProfileCard :profile="friend" friend />
        </div>
      </div>
    </section>
  </section>
</template>

<style scoped>
.title {
  font-weight: 600;
  font-size: 20px;
  text-align: center;
  margin: 0;
  margin-bottom: 30px;
}
.description {
  margin-left: 40px;
  font-weight: 500;
  font-size: 14px;
  color: var(--var-opposite-background-color);
  margin-bottom: 25px;
}
.profiles_wrap {
  padding: 0 40px;
}
.friend_card {
  margin-bottom: 20px;
}
</style>
