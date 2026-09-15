import apiClient from './apiClient'
import type { Product, ProductListResponse } from '../models/product'

export interface GetProductsParams {
  page?: number
  per_page?: number
  location?: string
}

export const productService = {
  getProducts: async (params?: GetProductsParams): Promise<ProductListResponse> => {
    const response = await apiClient.get<ProductListResponse>('/products', { params })
    return response.data
  },

  getProductById: async (id: number): Promise<Product> => {
    const response = await apiClient.get<Product>(`/products/${id}`)
    return response.data
  },
}
