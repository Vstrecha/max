import { ApiService } from '@/controllers/api'
import { notify } from '@/controllers/notifications'
import { VError } from '@/types/Error'
import type { EventsFilter, VExtendedEvent } from '@/types/Event'
import { VNotificationType } from '@/types/Notification'
import log from 'loglevel'
import { defineStore } from 'pinia'

const EVENTS_LOAD_PER_REQUEST = 10

const load_events = async (last_event_id?: string, events_filter?: EventsFilter) => {
  try {
    const new_events = await ApiService.events.get_events(
      EVENTS_LOAD_PER_REQUEST,
      last_event_id,
      events_filter?.tags,
      events_filter?.visability,
      events_filter?.repeatability,
    )
    return new_events
  } catch (error) {
    log.error(new VError("Can't load new events", error))
    notify(VNotificationType.ERROR, `Не смогли загрузить события по причине \n ${error}`)
    return Promise.reject(error)
  }
}

export const useGlobalEventsStore = defineStore('GlobalEvents', {
  state: () => ({
    events: [] as VExtendedEvent[],
    is_events_over: false,
    is_failed: false,
  }),

  actions: {
    async load_more_events(events_filter?: EventsFilter) {
      const last_event_id =
        this.events.length > 0 ? this.events[this.events.length - 1].event.id : undefined

      try {
        const new_events = await load_events(last_event_id, events_filter)

        this.events.push(...new_events.events)
        this.is_events_over = !new_events.has_more
      } catch {
        this.is_failed = true
      }
    },
    async reload_events(events_filter?: EventsFilter) {
      try {
        const new_events = await load_events(undefined, events_filter)

        this.events = new_events.events
        this.is_events_over = !new_events.has_more
      } catch {
        this.is_failed = true
      }
    },
  },
})
