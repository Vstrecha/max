import type { VExtendedEvent } from '@/types/Event'
import router from '@/router/router'

import { defineStore } from 'pinia'
import type { VProfile } from '@/types/Profile'

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
    openFriendRequestMode(invitation: string) {
      this.show_app = true
      router.push({ name: 'friend_request', params: { invitation } })
    },
    openAnonymousMode() {
      router.push({ name: 'welcome', params: { status: 'anonymous' } }).then(() => {
        this.show_app = true
        this.isFullscreen = true
      })
    },
    open_official() {
      router.push({ name: 'official' })
    },

    openInvitationMode(invitation: string) {
      router
        .push({ name: 'invitation', params: { invitation: invitation } })
        .then(() => (this.show_app = true))
      this.isFullscreen = true
    },
    openRegistrationMode(invitation: string) {
      router.push({ name: 'profile', hash: `#${invitation}`, params: { profile_id: 'new' } })
      this.isFullscreen = true
    },
    showWelcomePage() {
      router.push({ name: 'welcome', params: { status: 'new' } })
    },
    endRegistrationMode() {
      this.isFullscreen = false
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

    open_qr_code(event: VExtendedEvent) {
      alert('todo')
    },
  },
})
