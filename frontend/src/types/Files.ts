import * as v from 'valibot'

const VFileType = {
  AVATAR: 'avatar',
  EVENT: 'event',
} as const

type VFileTypeType = (typeof VFileType)[keyof typeof VFileType]

const VFileSchema = v.object({
  id: v.string(),
  url: v.string(),
})
type VFile = v.InferInput<typeof VFileSchema>

export { VFileSchema, VFileType }
export type { VFile, VFileTypeType }
