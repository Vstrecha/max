import * as v from 'valibot'

const EventVisability = {
  GLOBAL: 'G',
  PRIVATE: 'P',
} as const

type EventVisabilityType = (typeof EventVisability)[keyof typeof EventVisability]

const EventRepeatability = {
  NONE: 'N',
  REPEATABLE: 'R',
} as const

type EventRepeatabilityType = (typeof EventRepeatability)[keyof typeof EventRepeatability]

const EventStatus = {
  ACTIVE: 'A',
  ENDED: 'E',
} as const

type EventStatusType = (typeof EventStatus)[keyof typeof EventStatus]

type EventsFilter = {
  tags?: string[]
  visability?: EventVisabilityType
  repeatability?: EventRepeatabilityType
  status?: EventStatusType
}

const VEventSchema = v.object({
  id: v.string(),
  title: v.pipe(
    v.string(),
    v.nonEmpty('Заголовок не может быть пустым.'),
    v.maxLength(200, 'Заголовок не может превышать 200 символов.'),
  ),
  body: v.pipe(v.string(), v.nonEmpty('Описание не может быть пустым.')),
  photo_url: v.pipe(
    v.any(),
    v.transform((value) => (value === null ? undefined : value)), // null -> undefined
    v.optional(v.string()),
  ),
  photo: v.pipe(
    v.any(),
    v.transform((value) => (value === null ? undefined : value)), // null -> undefined
    v.optional(v.string()),
  ),
  tags: v.array(v.string()),

  place: v.pipe(
    v.any(),
    v.transform((value) => (value === null ? undefined : value)), // null -> undefined
    v.optional(v.string()),
  ),
  start_date: v.pipe(v.string(), v.isoDate('Дата должна быть в формате YYYY-MM-DD')),
  end_date: v.pipe(v.string(), v.isoDate('Дата должна быть в формате YYYY-MM-DD')),
  price: v.pipe(
    v.any(),
    v.transform((value) => (value === null ? undefined : value)), // null -> undefined
    v.optional(v.pipe(v.number(), v.minValue(0, 'Цена не может быть меньше нуля'))),
  ),
  participants: v.number(),
  creator: v.string(),
  visability: v.enum(EventVisability),
  repeatability: v.enum(EventRepeatability),
  status: v.enum(EventStatus),
  telegram_chat_link: v.pipe(
    v.any(),
    v.transform((value) => (value === null ? undefined : value)), // null -> undefined
    v.optional(v.string()),
  ),
})
type VEvent = v.InferInput<typeof VEventSchema>

const ParticipationType = {
  CREATOR: 'C',
  PARTICIPANT: 'P',
  VIEWER: 'V',
} as const

const VExtendedEventSchema = v.object({
  event: VEventSchema,
  friends_going: v.number(),
  participation_type: v.enum(ParticipationType),
})
type VExtendedEvent = v.InferInput<typeof VExtendedEventSchema>

const VExtendedEventsRespondSchema = v.object({
  events: v.array(VExtendedEventSchema),
  total: v.number(),
  has_more: v.boolean(),
})
type VExtendedEventsRespond = v.InferInput<typeof VExtendedEventsRespondSchema>

const VExtendedEventSkeleton = (): VExtendedEvent => ({
  event: {
    id: '1',
    title: '',
    body: '',
    photo: undefined,
    photo_url: undefined,
    price: undefined,
    place: undefined,
    telegram_chat_link: undefined,
    tags: [],
    start_date: new Date().toISOString().split('T')[0],
    end_date: new Date().toISOString().split('T')[0],
    participants: 0,
    creator: '',
    visability: 'G',
    repeatability: 'N',
    status: 'A',
  },
  friends_going: 0,
  participation_type: 'V',
})

export {
  EventVisability,
  EventRepeatability,
  EventStatus,
  VEventSchema,
  VExtendedEventSchema,
  ParticipationType,
  VExtendedEventSkeleton,
  VExtendedEventsRespondSchema,
}
export type {
  EventVisabilityType,
  EventRepeatabilityType,
  EventStatusType,
  VEvent,
  VExtendedEvent,
  EventsFilter,
  VExtendedEventsRespond,
}
