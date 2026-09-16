import apiClient from './apiClient'
import type { Order, OrderDetail, OrderListResponse, CreateOrderRequest } from '../models/order'

export interface GetOrdersParams {
  page?: number
  per_page?: number
}

export const orderService = {
  createOrder: async (data: CreateOrderRequest): Promise<Order> => {
    const response = await apiClient.post<Order>('/orders', data)
    return response.data
  },

  getOrderById: async (id: number): Promise<OrderDetail> => {
    const response = await apiClient.get<OrderDetail>(`/orders/${id}`)
    return response.data
  },

  getOrders: async (params?: GetOrdersParams): Promise<OrderListResponse> => {
    const response = await apiClient.get<OrderListResponse>('/orders', { params })
    return response.data
  },
}