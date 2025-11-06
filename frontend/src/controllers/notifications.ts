import { VNotificationType } from '@/types/Notification'
import { showNotify, type NotifyType } from 'vant'
import { haptic } from './max'
import type { VError } from '@/types/Error'
import log from 'loglevel'

const show = (type: NotifyType, message: string) =>
  showNotify({
    type,
    message,
  })

function notify_error(error: VError) {
  show('danger', error.message)
  log.warn(error.toString())
}

function notify(type: VNotificationType, message: string) {
  switch (type) {
    case VNotificationType.INFO:
      show('primary', message)
      break
    case VNotificationType.SUCCESS:
      show('success', message)
      break
    case VNotificationType.WARNING:
      show('warning', message)
      break
    case VNotificationType.ERROR:
      haptic.error()
      show('danger', message)
      break
  }
}

export { notify, notify_error }
