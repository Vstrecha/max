<template>
  <div class="information">
    <TextInput class="info_field" title="Имя" v-model="profile.first_name" :editing="isEditing" required />

    <TextInput class="info_field" title="Фамилия" v-model="profile.last_name" :editing="isEditing" required />

    <TextInput class="info_field" title="ВУЗ" v-model="profile.university" :editing="isEditing" required />

    <div v-if="isEditing">
      <TextInput class="info_field" title="Пол" v-model="profile.gender" :editing="isEditing" input_type="gender"
        required />
      <TextInput class="info_field" title="Дата рождения" v-model="profile.birth_date" :editing="isEditing" required
        input_type="date" />
    </div>

    <div v-if="!isEditing">
      <TextInput class="info_field" title="Возраст" v-model="get_full_age" :editing="isEditing" />

    </div>
  </div>
</template>

<script setup lang="ts">
import TextInput from '@/components/utility/TextInput.vue'
import type { VProfile } from '@/types/Profile'
import { useProfileActions } from '@/composables/useProfileActions'

defineProps<{
  isEditing: boolean
  isCreating: boolean

  friends?: VProfile[]
}>()
defineEmits<{
  (e: 'create_profile'): void
  (e: 'show_friends'): void
}>()
const profile = defineModel<VProfile>({ required: true })

const { get_full_age } = useProfileActions(profile)
</script>

<style scoped>
.information {
  margin-top: 10px;
  padding: 0 48px;
}

.info_field {
  margin-bottom: 25px;
}

.create_button_wrap {
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
}

.friends_wrap {
  width: 100%;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.friends_wrap:hover {
  cursor: pointer;
}

.friends_title {
  color: var(--var-secondary-emph-color);
  font-weight: 600;
  font-size: 20px;
}

.friends_list {
  margin-top: 13px;
  display: flex;
  justify-content: center;
  align-items: center;
  position: relative;
  padding-left: 11px;
}

.friend_avatar {
  position: relative;
  margin-left: -11px;
}

.friends_total {
  color: var(--var-opposite-background-color);
  font-weight: 400;
  font-size: 16px;
  margin-left: 6px;
}

.friends_extend_button {
  height: 80%;
}
</style>
