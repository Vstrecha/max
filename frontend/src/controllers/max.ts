const app = window.WebApp

const tg_state = {
  initDataRaw: undefined as string | undefined,
  startParam: undefined as string | undefined,

  user_first_name: undefined as string | undefined,
  user_last_name: undefined as string | undefined,
}


function init_app() {
  tg_state.initDataRaw = app.initData
  tg_state.startParam = app.initDataUnsafe.start_param
  tg_state.user_first_name = app.initDataUnsafe.user.first_name 
  tg_state.user_last_name = app.initDataUnsafe.user.last_name

  const platform = app.platform
  console.log(platform)
  if (platform == 'android' || platform == 'ios') {
    // request_fullscreen()
  }
}

const backButton = {
  show: () => app.BackButton.show(),
  hide: () => app.BackButton.hide(),
  addOnClick: (f: () => void) => {
    app.BackButton.onClick(f)
  },
}

const haptic = {
  button_click: () => {
    app.HapticFeedback.selectionChanged()
  },
  change_view: () => {
    app.HapticFeedback.impactOccurred('medium', false)
  },
  error: () => {
    app.HapticFeedback.notificationOccurred('medium', false)
  },
}

const share_url = (url: string, description: string) => {
  app.shareMaxContent(description, url)
}

// eslint-disable-next-line @typescript-eslint/no-explicit-any
const scan_qr = () : Promise<any> => {
  return app.openCodeReader(false);
}


init_app()
export { tg_state, haptic, share_url, scan_qr, backButton }
