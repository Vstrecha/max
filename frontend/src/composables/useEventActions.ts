import { notify } from '@/controllers/notifications'
import { haptic } from '@/controllers/max'
import { useAppStore } from '@/stores/appStore'
import {
  EventRepeatability,
  EventVisability,
  ParticipationType,
  type VExtendedEvent,
} from '@/types/Event'
import { VNotificationType } from '@/types/Notification'
import { computed, type Ref } from 'vue'

export function useEventActions(event: Ref<VExtendedEvent>) {
  const app_state = useAppStore()
  const get_participants = computed((): string => {
    const people_count = event.value.event.participants
    let people_count_string = ''
    if (people_count % 10 === 1 && people_count % 100 !== 11) {
      people_count_string = 'заинтересованный'
    } else {
      people_count_string = 'заинтересованных'
    }

    const friends_count = event.value.friends_going
    let friends_count_string = ''
    if (friends_count % 10 === 1 && friends_count % 100 !== 11) {
      friends_count_string = 'друг'
    } else if (
      friends_count % 10 >= 2 &&
      friends_count % 10 <= 4 &&
      (friends_count % 100 < 10 || friends_count % 100 >= 20)
    ) {
      friends_count_string = 'друга'
    } else {
      friends_count_string = 'друзей'
    }

    return (
      `${people_count} ${people_count_string}` +
      (friends_count != 0 ? ` (${friends_count} ${friends_count_string})` : '')
    )
  })

  const is_private = computed(() => event.value.event.visability == EventVisability.PRIVATE)
  const is_repeatable = computed(
    () => event.value.event.repeatability == EventRepeatability.REPEATABLE,
  )
  const is_creator = computed(() => event.value.participation_type == ParticipationType.CREATOR)
  const is_viewer = computed(() => event.value.participation_type == ParticipationType.VIEWER)

  const get_visability = computed(() =>
    event.value.event.visability == EventVisability.PRIVATE ? 'Приватное' : 'Публичное',
  )
  const get_repeatability = computed(() =>
    event.value.event.repeatability == EventRepeatability.REPEATABLE ? 'Регулярное' : 'Разовое',
  )

  const get_formatted_date = computed((): string => {
    const startDate = new Date(event.value.event.start_date)
    const endDate = new Date(event.value.event.end_date)

    const startDay = startDate.getDate()
    const endDay = endDate.getDate()
    const startMonth = startDate.toLocaleString('ru-RU', { month: 'short' })
    const endMonth = endDate.toLocaleString('ru-RU', { month: 'short' })
    const startYear = startDate.getFullYear()
    const endYear = endDate.getFullYear()

    if (startDay === endDay && startMonth === endMonth && startYear === endYear) {
      return `${startDay} ${startMonth} ${startYear}`
    }

    if (startMonth === endMonth && startYear === endYear) {
      return `${startDay}-${endDay} ${startMonth} ${startYear}`
    }

    return `${startDay} ${startMonth} - ${endDay} ${endMonth} ${endYear}`
  })

  const get_tags = computed((): string => event.value.event.tags.join(', '))

  const invite = function () {
    haptic.button_click()

    notify(VNotificationType.WARNING, 'Пока недоступно')
    return
    // ApiService.events
    //   .share_event(event.value.event)
    //   .then((link) => share_url(link, 'Давай сходим на эту встречу!'))
    //   .catch((error) =>
    //     notify(VNotificationType.ERROR, 'Не смогли получить ссылку на это событие ' + error),
    //   )
  }
  const open_extended_card = function () {
    haptic.button_click()
    app_state.openExtendedEventCard(event.value, true)
  }

  const open_qr = function () {
    haptic.button_click()
    const qr_text = event.value.event.telegram_chat_link ?? event.value.event.id
    const qr_description = `Покажи этот QR на «${event.value.event.title}»`
    app_state.openQRCode(qr_text, qr_description)
  }
  return {
    get_participants,
    get_formatted_date,
    get_tags,
    get_visability,
    get_repeatability,
    is_private,
    is_repeatable,
    is_creator,
    is_viewer,
    invite,
    open_extended_card,
    open_qr,
  }
}
