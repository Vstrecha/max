<script setup lang="ts">
import TabBar from '@/components/TabBar.vue'
import { useAppStore } from '@/stores/appStore'
import { tg_state } from '@/controllers/max'
import { useUserStore } from './stores/userStore'
import { ApiService } from './controllers/api'
import { onMounted, onUnmounted } from 'vue'
import { notify } from './controllers/notifications'
import { VNotificationType } from './types/Notification'

const app_state = useAppStore()
const user_state = useUserStore()

async function init() {
  try {
    user_state.profile = await ApiService.profile.my_profile()
  } catch (error) {
    notify(VNotificationType.ERROR, `Не смогли загрузить профиль. \n ${error}`)
    return
  }

  if (user_state.profile) {
    try {
      user_state.friends = await ApiService.friends.get(user_state.profile.id)
    } catch (error) {
      notify(VNotificationType.ERROR, `Не смогли загрузить список друзей. \n ${error}`)
      return
    }
    if (tg_state.startParam != undefined) {
      app_state.openFriendRequestMode(tg_state.startParam)
    }
  } else {
    app_state.openRegistrationMode()
  }
  app_state.show_app = true
}
const handleFocusIn = (e: FocusEvent) => {
  const target = e.target as HTMLElement
  if (target.tagName === 'INPUT' || target.tagName === 'TEXTAREA') {
    app_state.showTabBar = false
  }
}

const handleFocusOut = (e: FocusEvent) => {
  const target = e.target as HTMLElement
  if (target.tagName === 'INPUT' || target.tagName === 'TEXTAREA') {
    app_state.showTabBar = true
  }
}

onMounted(() => {
  window.addEventListener('focusin', handleFocusIn)
  window.addEventListener('focusout', handleFocusOut)
})

onUnmounted(() => {
  window.removeEventListener('focusin', handleFocusIn)
  window.removeEventListener('focusout', handleFocusOut)
})

init()
</script>

<template>
  <main
    class="main-app-container"
    :class="{ 'main-app-container-fullscreen': app_state.isFullscreen || !app_state.showTabBar }"
  >
    <RouterView v-slot="{ Component }">
      <Transition name="zoom-fade" mode="out-in">
        <component :is="Component" />
      </Transition>
    </RouterView>
  </main>
  <TabBar v-if="!app_state.isFullscreen && app_state.showTabBar" />
</template>

<style>
.main-app-container {
  --main-app-height: calc(100vh - 72px);
  height: var(--main-app-height);

  overflow: hidden;
}

.main-app-container-fullscreen {
  --main-app-height: 100vh;
}

.component-section-wrap {
  height: var(--main-app-height);
  overflow: auto;
  box-sizing: border-box;
}
.component-section {
  padding-top: 95px;
  padding-bottom: 35px;
}

.zoom-fade-enter-active,
.zoom-fade-leave-active {
  transition:
    transform 0.2s ease,
    opacity 0.2s ease;
}

.zoom-fade-enter-from,
.zoom-fade-leave-to {
  opacity: 0;
  transform: scale(0.97);
}

.zoom-fade-enter-to,
.zoom-fade-leave-from {
  opacity: 1;
  transform: scale(1);
}
</style>
