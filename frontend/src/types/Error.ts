type VErrorType = {
  message: string
  code?: number
  stack?: string
}

class VError implements VErrorType {
  message: string
  code?: number
  stack?: string
  data?: unknown

  constructor(message: string, data?: unknown, code?: number) {
    this.message = message
    this.code = code
    this.stack = new Error().stack
    this.data = data
  }

  toString(): string {
    return `Error: ${this.message} (Code: ${this.code}); ${JSON.stringify(this.data)}`
  }
}

export { VError, type VErrorType }
