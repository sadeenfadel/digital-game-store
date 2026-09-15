import { useState, useEffect, useCallback } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import type { OrderDetail } from '../../models/order'
import { orderService } from '../../services/orderService'
import { LoadingSpinner } from '../../components/LoadingSpinner'
import { ErrorMessage } from '../../components/ErrorMessage'
import { Header } from '../../components/Header'

export function ReceiptPage() {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()
  const [order, setOrder] = useState<OrderDetail | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  const fetchOrder = useCallback(async () => {
    if (!id) return
    setLoading(true)
    setError('')
    try {
      const data = await orderService.getOrderById(Number(id))
      setOrder(data)
    } catch (err: unknown) {
      if (err && typeof err === 'object' && 'response' in err) {
        const axiosErr = err as { response?: { status?: number } }
        if (axiosErr.response?.status === 404) {
          setError('Receipt not found.')
          return
        }
      }
      setError('Failed to load receipt. Please try again.')
    } finally {
      setLoading(false)
    }
  }, [id])

  useEffect(() => {
    fetchOrder()
  }, [fetchOrder])

  return (
    <div className="app">
      <Header />
      <main className="main-content">
        {loading && <LoadingSpinner message="Loading receipt..." />}
        {error && <ErrorMessage message={error} onRetry={fetchOrder} />}

        {!loading && !error && order && (
          <div className="receipt-page">
            <div className="receipt-card">
              <div className="receipt-success">
                <div className="receipt-check">&#10003;</div>
                <h1 className="receipt-title">Purchase Confirmed!</h1>
              </div>
              <div className="receipt-details">
                <div className="receipt-row">
                  <span className="receipt-label">Order ID</span>
                  <span className="receipt-value">#{order.id}</span>
                </div>
                <div className="receipt-row">
                  <span className="receipt-label">Product</span>
                  <span className="receipt-value">{order.product_title}</span>
                </div>
                <div className="receipt-row">
                  <span className="receipt-label">Product ID</span>
                  <span className="receipt-value">#{order.product_id}</span>
                </div>
                <div className="receipt-row">
                  <span className="receipt-label">Location</span>
                  <span className="receipt-value">{order.product_location}</span>
                </div>
                <div className="receipt-row receipt-total">
                  <span className="receipt-label">Price Paid</span>
                  <span className="receipt-value">${order.price_at_purchase}</span>
                </div>
                <div className="receipt-row">
                  <span className="receipt-label">Purchase Date</span>
                  <span className="receipt-value">
                    {new Date(order.created_at + 'Z').toLocaleString('en-GB', { timeZone: 'Asia/Amman' })}
                  </span>
                </div>
              </div>
              <button
                className="receipt-back-btn"
                onClick={() => navigate('/products')}
              >
                Back to Products
              </button>
            </div>
          </div>
        )}
      </main>
    </div>
  )
}
