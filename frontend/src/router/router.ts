import { createWebHistory, createRouter } from 'vue-router'

import WelcomeView from '@/views/WelcomeView.vue'
import FriendRequest from '@/components/utility/FriendRequest.vue'
import HomeView from '@/views/HomeView.vue'
import EventsView from '@/views/EventsView.vue'
import EventView from '@/views/EventView.vue'
import ProfileView from '@/views/ProfileView.vue'
import { backButton } from '@/controllers/max'
import FriendsView from '@/views/FriendsView.vue'
import QRCodeView from '@/views/QRCodeView.vue'

const routes = [
  {
    path: '/welcome/',
    name: 'welcome',
    component: WelcomeView,
  },
  {
    path: '/qr/:qr_code/:description',
    name: 'qr_code',
    props: true,
    component: QRCodeView,
    meta: { isPopup: true },
  },
  {
    path: '/',
    name: 'home',
    component: HomeView,
    children: [
      {
        path: 'friend_request/:invitation',
        name: 'friend_request',
        // Not the best solution
        meta: { isChildren: true },
        props: true,
        component: FriendRequest,
      },
    ],
  },
  {
    path: '/events',
    name: 'events',
    component: EventsView,
  },
  {
    path: '/event/new',
    name: 'create_event',
    component: EventView,
    props: { event_id: 'new' },
  },
  {
    path: '/event/:event_id',
    name: 'event_card',
    component: EventView,
    props: true,
    meta: { isPopup: true },
  },
  {
    path: '/profile/my',
    name: 'my_profile',
    component: ProfileView,
    props: { profile_id: 'my' },
  },
  {
    path: '/profile/:profile_id',
    name: 'profile',
    component: ProfileView,
    props: true,
    meta: { isPopup: true },
  },
  {
    path: '/profile/:profile_id/friends',
    name: 'profile_friends',
    component: FriendsView,
    props: true,
    meta: { isPopup: true },
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach((to) => {
  if (to.meta.isPopup) backButton.show()
  else backButton.hide()
  return true
})
backButton.addOnClick(() => router.back())

export default router
