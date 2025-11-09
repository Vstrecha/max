<template>
  <div class="information">
    <TextInput class="info_field" title="Имя" v-model="profile.first_name" :editing="isEditing" required />

    <TextInput class="info_field" title="Фамилия" v-model="profile.last_name" :editing="isEditing" required />

    <TextInput class="info_field" title="Пол" v-model="profile.gender" :editing="isEditing" input_type="gender" required />
    <TextInput class="info_field" title="Дата рождения" v-model="profile.birth_date" :editing="isEditing" required
      input_type="date" />

    <TextInput class="info_field" title="ВУЗ" v-model="profile.university" :editing="isEditing" required />

    <div v-if="!isEditing">
      <TextInput class="info_field" title="Возраст" v-model="get_full_age" :editing="isEditing" />

      <div class="friends_wrap" @click="show_friends">
        <div class="friends">
          <span class="friends_title">Друзья</span>
          <div class="friends_list">
            <AvatarImage class="friend_avatar" v-for="friend in friends?.slice(0, 4)" :key="friend.id"
              :avatar_url="friend.avatar_url" :signature="friend.first_name" width="27px" height="27px"
              border-weight="1" friend />
            <span class="friends_total"> ({{ friends?.length ?? 0 }}) </span>
          </div>
        </div>

        <img class="friends_extend_button" src="@/assets/icons/extend-list-button.svg" alt="Открыть" />
      </div>
    </div>
  </div>

  <Row justify="center" v-if="isCreating">
    <Col span="12">
    <div class="create_button_wrap">
      <Button type="primary" @click="send_create_profile">На Встречу!</Button>
    </div>
    </Col>
  </Row>
</template>

<script setup lang="ts">
import TextInput from '@/components/utility/TextInput.vue'
import { haptic } from '@/controllers/max'
import type { VProfile } from '@/types/Profile'
import { Col, Row, Button } from 'vant'
import AvatarImage from '../utility/AvatarImage.vue'
import { useProfileActions } from '@/composables/useProfileActions'

defineProps<{
  isEditing: boolean
  isCreating: boolean

  friends?: VProfile[]
}>()
const emit = defineEmits<{
  (e: 'create_profile'): void
  (e: 'show_friends'): void
}>()
const profile = defineModel<VProfile>({ required: true })

const { get_full_age } = useProfileActions(profile)

const send_create_profile = () => {
  haptic.button_click()
  emit('create_profile')
}

const show_friends = () => {
  haptic.button_click()
  emit('show_friends')
}
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
