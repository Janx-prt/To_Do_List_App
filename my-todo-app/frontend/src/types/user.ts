export interface User {
  id: number
  username: string
  email: string
  avatar: string
}

export interface CreateUserPayload {
  username: string
  email: string
  avatar: string
}
