<template>
  <div class="tabbar">
    <div class="tabs">
      <RouterLink v-slot="{ navigate, isActive }" custom :to="{ name: 'home' }">
        <div class="tab" @click="() => go(navigate)" :class="{ 'router-link-active': isActive }">
          <div class="tab_icon"><House :size="30" /></div>
          <span class="tab_name">Домой</span>
        </div>
      </RouterLink>
      <RouterLink v-slot="{ navigate, isActive }" custom :to="{ name: 'events' }">
        <div class="tab" @click="() => go(navigate)" :class="{ 'router-link-active': isActive }">
          <div class="tab_icon"><CalendarCheck2 :size="30" /></div>
          <span class="tab_name">События</span>
        </div>
      </RouterLink>
      <RouterLink v-slot="{ navigate, isActive }" custom :to="{ name: 'create_event' }">
        <div
          class="tab"
          id="add_event_tab"
          @click="() => go(navigate)"
          :class="{ 'router-link-active': isActive }"
        >
          <div id="add_event_icon">
            <img src="@/assets/icons/add-event-button.svg" />
          </div>
          <span class="tab_name">Добавить</span>
        </div>
      </RouterLink>
      <RouterLink v-slot="{ navigate, isActive }" custom :to="{ name: 'message_board' }">
        <div class="tab" @click="() => go(navigate)" :class="{ 'router-link-active': isActive }">
          <div class="tab_icon"><Handshake :size="30" /></div>
          <span class="tab_name">Объявления</span>
        </div>
      </RouterLink>
      <RouterLink v-slot="{ navigate, isActive }" custom :to="{ name: 'my_profile' }">
        <div class="tab" @click="() => go(navigate)" :class="{ 'router-link-active': isActive }">
          <div class="tab_icon"><User :size="30" /></div>
          <span class="tab_name">Профиль</span>
        </div>
      </RouterLink>
    </div>
    <div class="tab_space"></div>
  </div>
</template>

<style scoped>
.tabbar {
  position: fixed;
  z-index: 100;
  bottom: 0;
  left: 0;
  right: 0;
  width: 100%;
  height: 72px;
  background-color: var(--var-background-color);
  border-top: 1px solid #e2e1e1;

  display: block;

  font-size: 9px;
  font-weight: 600;
  letter-spacing: 0.16px;
}
.tabs {
  display: flex;
  align-items: end;

  height: 55px; /*72px-17px; */
}
.tab_space {
  height: 17px;
}
.tab {
  color: #e2e1e1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  width: 20%;
  margin: 0 2%;
}
.tab:hover {
  cursor: pointer;
}
.tab_name {
  margin-top: 6px;
}
#add_event_icon:hover {
  cursor: pointer;
}
#add_event_icon {
  margin-bottom: 7px;
}
.router-link-active {
  color: var(--var-secondary-emph-color);

  animation: pulse;
  animation-duration: 0.4s;
}
</style>

<script setup lang="ts">
import { House, CalendarCheck2, Handshake, User } from 'lucide-vue-next'
import { haptic } from '@/controllers/max'

const go = function (navigate: () => void) {
  haptic.change_view()
  navigate()
}
</script>
