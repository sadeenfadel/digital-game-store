import apiClient from './apiClient'
import type { LoginRequest, LoginResponse } from '../models/user'

export const authService = {
  login: async (data: LoginRequest): Promise<LoginResponse> => {
    const response = await apiClient.post<LoginResponse>('/auth/login', data)
    return response.data
  },
}
