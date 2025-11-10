<script setup lang="ts">
import { type VExtendedEvent } from '@/types/Event'
import IconedTextField from '@/components/utility/IconedTextField.vue'
import { useEventActions } from '@/composables/useEventActions'

import { MapPin, CalendarClock, Users } from 'lucide-vue-next'
import { Image as VanImage } from 'vant'
import { toRef } from 'vue'

const props = defineProps<{
  extended_event: VExtendedEvent
}>()

// TODO move it to class
const {
  get_participants,
  is_viewer,
  get_formatted_date,
  get_tags,
  open_extended_card,
  open_qr,
} = useEventActions(toRef(props, 'extended_event'))

const event = props.extended_event.event
</script>

<template>
  <div class="event_card event-card" @click="open_extended_card">
    <div class="event_head">
      <div class="event_title_wrap">
        <h3 class="event_title">{{ event.title }}</h3>
        <div class="event_tags">
          {{ get_tags }}
        </div>
      </div>
    </div>
    <div class="event_body">
      <div class="event_body_photo">
        <vanImage fit="cover" radius="10px" width="100px" height="100px" :src="event.photo_url" />
      </div>
      <div class="event_body_info_wrap">
        <IconedTextField :text="event.place || ''">
          <MapPin :size="17" color="var(--var-secondary-emph-color)" />
        </IconedTextField>
        <IconedTextField :text="get_formatted_date">
          <CalendarClock :size="17" color="var(--var-secondary-emph-color)" />
        </IconedTextField>
        <IconedTextField :text="get_participants">
          <Users :size="17" color="var(--var-secondary-emph-color)" />
        </IconedTextField>
      </div>
    </div>
    <div v-if="!is_viewer" class="event_buttons_wrap">
      <div class="event_button" @click.stop="open_qr"><span>Открыть QR-код</span></div>
    </div>
  </div>
</template>

<style>
.event_card {
  margin: 11px 0;
  width: 100%;
  background: var(--var-small-parts-background-color);
  border-radius: 10px;
}
.event-card .event_card:hover {
  cursor: pointer;
}

.event-card .event_head {
  position: relative;

  margin: 14px 18px;
  color: var(--var-opposite-background-color);
}

.event-card .event_title {
  margin: 0;
  margin-right: 42px;
  margin-bottom: 1px;
  font-weight: 600;
  font-size: 17px;
}
.event-card .event_tags {
  font-weight: 500;
  font-size: 8px;

  opacity: 0.6;
}
.event-card .event_marks {
  position: absolute;
  top: 0;
  right: 0;
}
.event-card .event_marks > * {
  display: inline-block;
}
.event-card .event_marks_space {
  width: 5px;
}

.event-card .event_body {
  margin: 18px;
  margin-top: 0;
  display: flex;
}

.event-card .event_body_photo {
  filter: drop-shadow(4px 4px 8px rgba(0, 0, 0, 0.6));
}
.event-card .event_body_info_wrap {
  display: inline-flex;
  flex-direction: column;
  justify-content: space-between;
  margin: 5px 0;
  margin-left: 15px;

  height: auto;
}

.event-card .event_buttons_wrap {
  background: var(--var-primary-emph-color);
  border-radius: 0 0 10px 10px;
  display: flex;
  justify-content: center;
}
.event-card .event_button_space {
  width: 3px;
  height: auto;

  background: var(--var-small-parts-background-color);
}

.event-card .event_button {
  padding: 9px 0;
  width: 100%;
  text-align: center;
  font-weight: 700;
  font-size: 10px;
  color: var(--var-background-color);
}
.event-card .event_button:hover {
  cursor: pointer;
}
</style>
