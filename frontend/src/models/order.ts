export interface Order {
  id: number
  product_id: number
  product_title: string
  price: string
  location: string
  created_at: string
}

export interface OrderDetail {
  id: number
  product_id: number
  product_title: string
  price_at_purchase: string
  product_location: string
  created_at: string
  user_id: number
}

export interface CreateOrderRequest {
  product_id: number
}
