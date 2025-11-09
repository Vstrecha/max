import {
  VEventSchema,
  VExtendedEventsRespondSchema,
  type EventRepeatabilityType,
  type EventVisabilityType,
  type VEvent,
  type VExtendedEventsRespond,
} from '@/types/Event'
import { tg_state } from './max'
import {
  VProfileOrUndefinedSchema,
  VProfileSchema,
  type VCreateProfile,
  type VProfile,
  type VProfileOrUndefined,
} from '@/types/Profile'
import { VError } from '@/types/Error'

import * as v from 'valibot'
import axios from 'axios'
import { v4 as uuidv4 } from 'uuid'
import log from 'loglevel'
import { VFileSchema, type VFile, type VFileTypeType } from '@/types/Files'

const XRequestId = generate_request_id()
const tmaToken = tg_state.initDataRaw

const apiClient = axios.create({
  baseURL: 'https://max-total.ru/api/v1',
  headers: {
    'Content-Type': 'application/json',
    'X-Request-Id': XRequestId,
    Authorization: `tma ${tmaToken}`,
  },
  responseType: 'json',
})

apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response) {
      // Парсим ответ с ошибкой
      const parsedResponse = v.safeParse(v.string(), error.response.data?.detail)
      if (parsedResponse.success) {
        // Возвращаем ожидаемую ошибку
        return Promise.reject(parsedResponse.output)
      } else {
        // Если ответ не соответствует ожидаемой схеме
        return Promise.reject({
          code: 'UNKNOWN_ERROR',
          details: 'Неизвестная ошибка сервера',
        })
      }
    } else if (error.request) {
      // Ошибка, связанная с запросом (например, нет ответа от сервера)
      return Promise.reject({
        code: 'NETWORK_ERROR',
        details: 'Ошибка сети или сервер недоступен',
      })
    } else {
      // Ошибка, возникшая при настройке запроса
      return Promise.reject({
        code: 'REQUEST_ERROR',
        details: error.message,
      })
    }
  },
)

const EventsApi = {
  async select_event(event_id: string): Promise<VEvent> {
    const url = `events/user_events/${event_id}`
    const response = await apiClient.post(url)
    return parse_response(VEventSchema, response.data)
  },
  async deselect_event(event_id: string): Promise<string> {
    const url = `events/user_events/${event_id}`
    const response = await apiClient.delete(url)
    return parse_response(v.string(), response.data?.message)
  },
  async create_event(event: VEvent): Promise<VEvent> {
    const url = `/events/global_events/`
    const response = await apiClient.post(url, event)
    return parse_response(VEventSchema, response.data)
  },
  async edit_event(event: VEvent): Promise<VEvent> {
    const url = `/events/global_events/${event.id}`
    const response = await apiClient.patch(url, event)
    return parse_response(VEventSchema, response.data)
  },
  async get_events(
    limit: number,
    last_event_id?: string,
    tags?: string[],
    visability?: EventVisabilityType,
    repeatability?: EventRepeatabilityType,
  ): Promise<VExtendedEventsRespond> {
    const url = `/events/global_events/`
    const params = {
      limit,
      last_event_id,
      tags,
      visability,
      repeatability,
    }
    const response = await apiClient.get(url, { params })
    return parse_response(VExtendedEventsRespondSchema, response.data)
  },
  async get_user_events(
    limit: number,
    last_event_id?: string,
    tags?: string[],
    visability?: EventVisabilityType,
    repeatability?: EventRepeatabilityType,
  ): Promise<VExtendedEventsRespond> {
    const url = `/events/user_events/`
    const params = {
      limit,
      last_event_id,
      tags,
      visability,
      repeatability,
    }
    const response = await apiClient.get(url, { params })
    return parse_response(VExtendedEventsRespondSchema, response.data)
  },
  async share_event(event: VEvent): Promise<string> {
    const url = `/user_events/share/${event.id}/`
    const response = await apiClient.post(url)
    return parse_response(v.string(), response.data?.event_public_url)
  },
}

const ProfileApi = {
  async my_profile(): Promise<VProfileOrUndefined> {
    const url = `/profiles/my`
    const response = await apiClient.get(url)
    return parse_response(VProfileOrUndefinedSchema, response.data)
  },
  async load_profile(profile_id: string): Promise<VProfile> {
    const url = `/profiles/${profile_id}`
    const response = await apiClient.get(url)
    return parse_response(VProfileSchema, response.data)
  },
  async create_profile(new_profile: VCreateProfile): Promise<VProfile> {
    const url = `/profiles/`
    const response = await apiClient.post(url, new_profile)
    return parse_response(VProfileSchema, response.data)
  },
  // :NOTE: VProfile contains unnessusary fields
  async update_profile(profile: VProfile): Promise<VProfile> {
    const url = `/profiles/`
    const response = await apiClient.patch(url, profile)
    return parse_response(VProfileSchema, response.data)
  },
}

const FriendsApi = {
  async check_invitation(invitation: string): Promise<VProfile> {
    const url = `/friends/check/${invitation}`
    const response = await apiClient.get(url)
    return parse_response(VProfileSchema, response.data)
  },
  async create_invitation(): Promise<string> {
    const url = `/friends/new`
    const response = await apiClient.get(url)
    return parse_response(v.string(), response.data?.id)
  },
  async get(profile_id: string): Promise<VProfile[]> {
    const url = `/friends/list/${profile_id}`
    const response = await apiClient.get(url)
    return parse_response(v.array(VProfileSchema), response.data)
  },
  async add(invitation: string): Promise<string> {
    const url = `/friends/new`
    const response = await apiClient.post(url, { invitation_id: invitation })
    return parse_response(v.string(), response.data?.id)
  },
}

const FilesApi = {
  async upload_file(file: File, type: VFileTypeType): Promise<VFile> {
    const url = `/files/upload`

    const formData = new FormData()

    formData.append('file', file)
    formData.append('file_type', type)

    const response = await apiClient.post(url, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
    return parse_response(VFileSchema, response.data)
  },
}

const ApiService = {
  events: EventsApi,
  profile: ProfileApi,
  friends: FriendsApi,

  files: FilesApi,
  // Documents
  //   async addDoc(doc: Doc): Promise<string> {
  //     const url = `/docs/`
  //     const response = await apiClient.post(url, { doc })
  //     return parse_response(v.string(), response)
  //   },
}

// function gen_response_error(error_msg: string): Promise<IApiError> {
//   return Promise.reject({ message: error_msg, error_code: 'SERVER_INVALID_RESPONSE', XRequestId })
// }

function generate_request_id(): string {
  return uuidv4()
}

// response: AxiosResponse<unknown, unknown>,
function parse_response<const TSchema extends v.BaseSchema<unknown, unknown, v.BaseIssue<unknown>>>(
  schema: TSchema,
  response: unknown,
): Promise<v.InferOutput<TSchema>> {
  const parsed_response = v.safeParse(schema, response)
  if (parsed_response.success) {
    return Promise.resolve(parsed_response.output)
  } else {
    log.error(new VError("Can't parse server respond", { r: response, s: parsed_response.issues }))

    return Promise.reject(parsed_response.issues[0].message)
  }
}

export { ApiService, XRequestId }
