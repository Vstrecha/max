import {
  init,
  postEvent,
  initData,
  shareURL,
  hapticFeedback,
  openTelegramLink,
  backButton as maxBackButton,
  requestWriteAccess,
  miniApp,
} from '@telegram-apps/sdk'

init()

const max_state = {
  initDataRaw: undefined as string | undefined,
  startParam: undefined as string | undefined,
}

// TODO it looks like max.api should't care about window.location
const hash = window.location.hash.slice(1)

function init_max_app() {
  initData.restore()

  max_state.initDataRaw = initData.raw()
  max_state.startParam = initData.startParam()

  const params = new URLSearchParams(hash)
  const platform = params.get('tgWebAppPlatform')
  console.log(platform)
  if (platform == 'android' || platform == 'ios') {
    request_fullscreen()
  }
}
if (maxBackButton.mount.isAvailable()) {
  maxBackButton.mount()
}

if (miniApp.mountSync.isAvailable()) {
  miniApp.mountSync()
  miniApp.ready.ifAvailable()
}

const create_bot_contact = async (): Promise<string> => {
  if (requestWriteAccess.isAvailable()) {
    const status = await requestWriteAccess()
    return status === 'allowed' ? Promise.resolve(status) : Promise.reject(status)
  }
  return Promise.reject('none')
}

const request_fullscreen = () => {
  postEvent('web_app_request_fullscreen')
}

const backButton = {
  show: () => maxBackButton.show.ifAvailable(),
  hide: () => maxBackButton.hide.ifAvailable(),
  addOnClick: (f: () => void) => {
    if (maxBackButton.onClick.isAvailable()) maxBackButton.onClick(f)
  },
}

const haptic = {
  button_click: () => {
    if (hapticFeedback.selectionChanged.isAvailable()) {
      hapticFeedback.selectionChanged()
    }
  },
  change_view: () => {
    if (hapticFeedback.impactOccurred.isAvailable()) {
      hapticFeedback.impactOccurred('medium')
    }
  },
  error: () => {
    if (hapticFeedback.notificationOccurred.isAvailable()) {
      hapticFeedback.notificationOccurred('error')
    }
  },
}

const share_url = (url: string, description: string) => {
  if (shareURL.isAvailable()) {
    shareURL(url, description)
  }
}

const open_max_link = (url: string) => {
  if (openTelegramLink.isAvailable()) {
    openTelegramLink(url)
  }
}

init_max_app()
export { max_state, haptic, share_url, open_max_link, backButton, create_bot_contact }
