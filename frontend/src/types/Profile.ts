import * as v from 'valibot'

const nullable_string = v.pipe(
  v.any(),
  v.transform((value) => (value === null ? undefined : value)),
  v.optional(v.string()),
)

const VProfileSchema = v.object({
  id: v.string(),
  first_name: v.pipe(v.string(), v.nonEmpty('Имя не может быть пустым.')),
  last_name: v.pipe(v.string(), v.nonEmpty('Фамилия не может быть пустой.')),
  birth_date: v.pipe(
    v.string(),
    v.isoDate('Дата должна быть в формате YYYY-MM-DD'),
    v.maxValue('2008-09-01', 'На Встречи! ходят только с 17-ти лет.'),
  ),
  gender: v.pipe(v.string(), v.values(['M', 'F'], 'Пол должен быть выбран')),
  university: v.pipe(v.string(), v.nonEmpty('Поле ВУЗ не может быть пустым.')),
  avatar: nullable_string,
  avatar_url: nullable_string,
  is_superuser: v.boolean(),
})
type VProfile = v.InferOutput<typeof VProfileSchema>

const VProfileOrUndefinedSchema = v.pipe(
  v.union([VProfileSchema, v.pipe(v.string(), v.empty())]),
  v.transform((input) => (typeof input === 'string' ? undefined : input)),
)
type VProfileOrUndefined = v.InferOutput<typeof VProfileOrUndefinedSchema>

type VCreateProfile = {
  first_name: string
  last_name: string
  gender: string // 'M' | 'F'
  birth_date: string
  avatar: string | undefined
  university: string
}

const VProfileSkeleton = (): VProfile => ({
  id: '',
  first_name: '',
  last_name: '',
  birth_date: '',
  gender: 'M',
  avatar: undefined,
  avatar_url: undefined,
  university: '',
  is_superuser: false,
})

export { VProfileSchema, VProfileSkeleton, VProfileOrUndefinedSchema }
export type { VProfile, VCreateProfile, VProfileOrUndefined }
