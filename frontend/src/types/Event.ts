import * as v from 'valibot'

const EventStatus = {
  ACTIVE: 'A',
  ENDED: 'E',
} as const

type EventStatusType = (typeof EventStatus)[keyof typeof EventStatus]

type EventsFilter = {
  tags?: string[]
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

  participants: v.number(),
  max_participants: v.pipe(
    v.any(),
    v.transform((value) => (value === null ? undefined : value)), // null -> undefined
    v.optional(v.number()),
  ),
  creator: v.string(),
  registration_start_date: v.pipe(
    v.any(),
    v.transform((value) => (value === null ? undefined : value)), // null -> undefined
    v.optional(
      v.pipe(
        v.string(),
        v.check((input) => !Number.isNaN(Date.parse(input)), 'Дата и время должны быть валидными.'),
      ),
    ),
  ),
  registration_end_date: v.pipe(
    v.any(),
    v.transform((value) => (value === null ? undefined : value)), // null -> undefined
    v.optional(
      v.pipe(
        v.string(),
        v.check((input) => !Number.isNaN(Date.parse(input)), 'Дата и время должны быть валидными.'),
      ),
    ),
  ),
  status: v.enum(EventStatus),
  is_registration_available: v.pipe(
    v.any(),
    v.transform((value) => (value === null ? false : value)),
    v.boolean(),
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
  participation_id: v.pipe(
   v.any(),
    v.transform((value) => (value === null ? undefined : value)), // null -> undefined
    v.optional(
      v.string()
  )),
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
    place: undefined,
    tags: [],
    start_date: new Date().toISOString().split('T')[0],
    end_date: new Date().toISOString().split('T')[0],
    participants: 0,
    max_participants: undefined,
    registration_start_date: undefined,
    registration_end_date: undefined,
    creator: '',
    status: 'A',
    is_registration_available: true,
  },
  friends_going: 0,
  participation_type: 'V',
  participation_id: undefined,  
})

const VQRResultSchema = v.object({
  user_id: v.string(),
  event_id: v.string(),
})

type VQRResult = v.InferInput<typeof VQRResultSchema>

export {
  EventStatus,
  VEventSchema,
  VExtendedEventSchema,
  ParticipationType,
  VExtendedEventSkeleton,
  VExtendedEventsRespondSchema,
  VQRResultSchema,
}
export type {
  EventStatusType,
  VEvent,
  VExtendedEvent,
  EventsFilter,
  VExtendedEventsRespond,
  VQRResult,
}
