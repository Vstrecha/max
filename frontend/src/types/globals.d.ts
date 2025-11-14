/* eslint-disable @typescript-eslint/no-explicit-any */
interface Window {
  WebApp: {
    initData: string
    initDataUnsafe: any
    platform: string
    ready: () => void
    shareMaxContent: (text: string, link: string) => void
    openCodeReader: (fileSelect: boolean) => string  
    BackButton: {
      isVisible: boolean
      show: () => void
      hide: () => void
      onClick: any
    }
    HapticFeedback: {
      selectionChanged: () => void
      notificationOccurred: (notificationType: string, disableVibrationFallback: boolean) => void
      impactOccurred: (impactStyle: string, disableVibrationFallback: boolean) => void
    }
  }
}
