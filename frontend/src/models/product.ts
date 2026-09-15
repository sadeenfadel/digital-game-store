export type Location = 'JO' | 'SA'

export interface Product {
  id: number
  title: string
  description: string | null
  price: string
  location: Location
  created_at: string
  updated_at: string
}

export interface Pagination {
  page: number
  per_page: number
  total: number
  pages: number
}

export interface ProductListResponse {
  items: Product[]
  pagination: Pagination
}
