import type { VEvent } from '@/types/Event'

const dateTimeFormatter = new Intl.DateTimeFormat('ru-RU', {
  dateStyle: 'medium',
  timeStyle: 'short',
})

export const parseEventDateTime = (value: string | undefined): Date | undefined => {
  if (!value) return undefined
  const parsed = new Date(value)
  if (Number.isNaN(parsed.getTime())) return undefined
  return parsed
}

export const normalizeDateTimeForApi = (value: string | undefined): string | undefined => {
  if (!value) return undefined
  return value.length === 16 ? `${value}:00` : value
}

export const getRegistrationBlockReason = (event: VEvent): string | undefined => {
  const now = new Date()
  const start = parseEventDateTime(event.registration_start_date)
  if (start && now < start) {
    return `Регистрация откроется ${dateTimeFormatter.format(start)}`
  }

  const end = parseEventDateTime(event.registration_end_date)
  if (end && now > end) {
    return 'Регистрация уже завершена'
  }

  if (event.max_participants && event.participants >= event.max_participants) {
    return 'Достигнуто максимальное количество участников'
  }

  return undefined
}

export const isRegistrationWindowOpen = (event: VEvent): boolean =>
  getRegistrationBlockReason(event) === undefined

export const getRegistrationState = (event: VEvent) => {
  const reason = getRegistrationBlockReason(event)
  return {
    isAvailable: reason === undefined,
    reason,
  }
}
