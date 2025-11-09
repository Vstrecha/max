<script setup lang="ts">
import type { VProfile } from '@/types/Profile'
import AvatarImage from '../utility/AvatarImage.vue'
import { computed, toRef } from 'vue'
import { useProfileActions } from '@/composables/useProfileActions'

const props = defineProps<{
  profile: VProfile
  friend?: boolean
  removable?: boolean
}>()

const { get_full_age, get_name } = useProfileActions(toRef(props, 'profile'))

const get_info = computed(() => {
  return `${get_full_age.value}, ${props.profile.university}`
})

const get_color = computed(() =>
  props.friend ? 'var(--var-secondary-emph-color)' : 'var(--var-primary-emph-color)',
)
</script>

<template>
  <div class="profile_card">
    <AvatarImage
      width="47px"
      height="47px"
      border-weight="2"
      :signature="profile.name"
      :avatar_url="profile.avatar_url"
      :friend="friend"
    />
    <div class="profile_inforamtion">
      <h5 class="profile_name" :style="{ color: get_color }">{{ get_name }}</h5>
      <span class="profile_data">{{ get_info }}</span>
    </div>

    <!-- <img class="friends_extend_button" src="@/assets/icons/extend-list-button.svg" alt="Открыть" /> -->
  </div>
</template>

<style scoped>
.profile_card {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.profile_card:hover {
  cursor: pointer;
}
.profile_inforamtion {
  flex-grow: 1;

  display: flex;
  flex-direction: column;
  align-items: self-start;
  justify-content: center;
  margin-left: 12px;
}
.profile_name {
  font-weight: 500;
  font-size: 17px;
  margin: 0;
  margin-bottom: 5px;
}
.profile_data {
  font-weight: 400;
  font-size: 14px;
  color: var(--var-opposite-background-color);
}
</style>
