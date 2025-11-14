import router from '@/router/router'

import { defineStore } from 'pinia'
import type { VProfile } from '@/types/Profile'
import type { VExtendedEvent } from '@/types/Event'

const add_position = (callback: () => void) => {
  const currentPath = router.currentRoute.value.path
  const currentScroll = document.querySelector('.component-section-wrap')?.scrollTop
  if (currentScroll !== undefined)
    router.push({ path: currentPath, hash: `#${currentScroll}` }).then(callback)
}

export const useAppStore = defineStore('App', {
  state: () => ({
    show_app: false,
    isFullscreen: false,
    showTabBar: true,
    activeEventCard: undefined as VExtendedEvent | undefined,
    activeFriendRequest: undefined as VProfile | undefined,
  }),
  actions: {
    openRegistrationMode() {
      router.push({ name: 'welcome' }).then(() => (this.show_app = true))
      this.isFullscreen = true
    },
    endRegistrationMode() {
      this.isFullscreen = false
      this.show_app = true
      router.push({ name: 'home' })
    },

    openExtendedEventCard(event: VExtendedEvent, save_position = true) {
      this.activeEventCard = event
      const new_route = () =>
        router.push({ name: 'event_card', params: { event_id: event.event.id } })
      if (save_position) {
        add_position(new_route)
      } else new_route()
    },

    openFriendsList(profile_id: string) {
      router.push({ name: 'profile_friends', params: { profile_id: profile_id } })
    },
    openProfilePage(profile_id: string) {
      router.push({ name: 'profile', params: { profile_id: profile_id } })
    },

    openQRCode(qr_code: string, description?: string) {
      router.push({
        name: 'qr_code',
        params: {
          qr_code,
          description,
        },
      })
    },
  },
})
