import { ApiService } from '@/controllers/api'
import { share_url } from '@/controllers/max'
import type { VProfile } from '@/types/Profile'
import { defineStore } from 'pinia'

export const ALL_TAGS = ['Лекция', 'Музей', 'Спорт', 'Музыка', 'Природа']

export const useUserStore = defineStore('User', {
  state: () => ({
    profile: undefined as VProfile | undefined,
    friends: undefined as VProfile[] | undefined,
  }),
  actions: {
    async create_invitation() {
      const invitation = await ApiService.friends.create_invitation()
      const tg_url = `https://t.me/stud_vstrecha_bot?startapp=${invitation}`
      share_url(tg_url, 'Приглашаю в друзья в приложении Встреча!')
    },
  },
})
