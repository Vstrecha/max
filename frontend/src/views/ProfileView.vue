<template>
  <section class="component-section-wrap">
    <section class="component-section">
      <img class="component-background-1" src="@/assets/icons/background-effect-1.svg" />
      <div v-if="profile != undefined" class="content">
        <ProfileHeader
          v-model="profile"
          :is-creating="states.isCreating"
          :is-editable="states.isEditable"
          :is-editing="states.isEditing"
          @save_changes="save_changes"
          @start_editing="start_editing"
        />

        <ProfileInformation
          :is-editing="states.isEditing"
          :is-creating="states.isCreating"
          v-model="profile"
          :friends="friends"
          @create_profile="create_profile"
          @show_friends="open_friends_page"
        />

      </div>
      <CentralLoader v-else />
    </section>
  </section>
</template>

<style scoped>

.component-section-wrap {
  position: relative;
}

.component-background-1 {
  position: absolute;
  top: 0;
  right: 0;
  z-index: 0;
}
.component-section {
  position: relative;
}
.content {
  position: relative;
  z-index: 10;
}
</style>

<script lang="ts" setup>
import { haptic } from '@/controllers/max'
import {
  VProfileSchema,
  VProfileSkeleton,
  type VCreateProfile,
  type VProfile,
} from '@/types/Profile'

import CentralLoader from '@/components/utility/CentralLoader.vue'
import { ApiService } from '@/controllers/api'

import ProfileHeader from '@/components/Profile/ProfileHeader.vue'
import ProfileInformation from '@/components/Profile/ProfileInformation.vue'
import { notify } from '@/controllers/notifications'
import { useUserStore } from '@/stores/userStore'
import { VNotificationType } from '@/types/Notification'
import * as v from 'valibot'
import { ref, watch, type Ref } from 'vue'
import { useAppStore } from '@/stores/appStore'

const props = defineProps<{
  profile_id: string
}>()

const user_state = useUserStore()
const app_state = useAppStore()

const profile: Ref<VProfile | undefined> = ref(undefined)
const friends: Ref<VProfile[] | undefined> = ref(undefined)
const states = ref({
  isEditing: false,
  isEditable: false,
  isCreating: false,
})

const start_editing = () => (states.value.isEditing = true)
const save_changes = () => {
  if (!validate_profile()) return

  states.value.isEditing = false
  update_profile()
}

const validate_profile = (): boolean => {
  const validation = v.safeParse(VProfileSchema, profile.value)
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

const load_profile = (profile_id: string) => {
  ApiService.profile
    .load_profile(profile_id)
    .then((loaded_profile) => {
      profile.value = loaded_profile
      if (loaded_profile.id === user_state.profile?.id) {
        states.value.isEditable = true
      }
    })
    .catch((error) => {
      notify(VNotificationType.ERROR, `Не получилось загрузить профиль. \n ${error}`)
    })
}

const load_my_profile = () => {
  ApiService.profile
    .my_profile()
    .then((loaded_profile) => {
      profile.value = loaded_profile
      user_state.profile = loaded_profile
    })
    .catch((error) => notify(VNotificationType.ERROR, `Не смогли найти ваш профиль. \n ${error}`))
}

const load_friends = (profile_id: string) => {
  ApiService.friends
    .get(profile_id)
    .then((loaded_friends) => {
      friends.value = loaded_friends
    })
    .catch((error) =>
      notify(VNotificationType.ERROR, `Не смогли загрузить список друзей. \n ${error}`),
    )
}

const create_profile = () => {
  haptic.button_click()
  if (!validate_profile() || profile.value == undefined) return

  const new_profile: VCreateProfile = {
    first_name: profile.value.first_name,
    last_name: profile.value.last_name,
    gender: profile.value.gender,
    birth_date: profile.value.birth_date,
    avatar: profile.value.avatar,
    university: profile.value.university,
  }
  ApiService.profile
    .create_profile(new_profile)
    .then((created_profile) => {
      user_state.profile = created_profile
      notify(VNotificationType.SUCCESS, `${created_profile.first_name}, твой профиль создан!`)
      app_state.endRegistrationMode()
    })
    .catch((error) => {
      notify(VNotificationType.ERROR, `Не получилось создать профиль профиль. \n ${error}`)
    })
}

const update_profile = () => {
  if (profile.value == undefined) return

  ApiService.profile
    .update_profile(profile.value)
    .then((updated_profile) => {
      notify(VNotificationType.SUCCESS, 'Профиль обновлён!')
      user_state.profile = updated_profile
    })
    .catch((error) => {
      notify(VNotificationType.ERROR, `Не получилось обновить профиль. \n ${error}`)
    })
}

const open_friends_page = () => {
  if (profile.value) app_state.openFriendsList(profile.value.id)
}


function init() {
  states.value.isEditing = false
  states.value.isEditable = false
  states.value.isCreating = false

  if (props.profile_id == 'my') {
    states.value.isEditable = true
    profile.value = user_state.profile
    load_my_profile()
    friends.value = user_state.friends
    if (profile.value) load_friends(profile.value?.id)
  } else if (props.profile_id == 'new') {
    states.value.isEditing = true
    states.value.isCreating = true
    profile.value = VProfileSkeleton()
  } else {
    load_profile(props.profile_id)
    load_friends(props.profile_id)
  }
}

init()
watch(() => props.profile_id, init)
</script>
