import apiClient from './apiClient'
import type { Order, OrderDetail, CreateOrderRequest } from '../models/order'

export const orderService = {
  createOrder: async (data: CreateOrderRequest): Promise<Order> => {
    const response = await apiClient.post<Order>('/orders', data)
    return response.data
  },

  getOrderById: async (id: number): Promise<OrderDetail> => {
    const response = await apiClient.get<OrderDetail>(`/orders/${id}`)
    return response.data
  },
}
