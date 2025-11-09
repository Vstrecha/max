import type { VProfile } from '@/types/Profile'
import { computed, type Ref } from 'vue'

function get_years_string(years: number) {
  const lastDigit = years % 10
  const lastTwoDigits = years % 100

  if (lastDigit === 1 && lastTwoDigits !== 11) {
    return `${years} год`
  } else if (lastDigit >= 2 && lastDigit <= 4 && (lastTwoDigits < 12 || lastTwoDigits > 14)) {
    return `${years} года`
  } else {
    return `${years} лет`
  }
}

export function useProfileActions(profile: Ref<VProfile>) {
  const get_full_age = computed(() => {
    const date = new Date(profile.value.birth_date)
    const currentDate = new Date()

    const yearsPassed =
      currentDate.getFullYear() -
      date.getFullYear() -
      (currentDate.getMonth() < date.getMonth() ||
      (currentDate.getMonth() === date.getMonth() && currentDate.getDate() < date.getDate())
        ? 1
        : 0)

    return get_years_string(yearsPassed)
  })
  const get_name = computed(() => profile.value.first_name + profile.value.last_name)
  return {
    get_full_age,
    get_name,
  }
}
