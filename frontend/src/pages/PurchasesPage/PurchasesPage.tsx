import { useState, useEffect, useCallback } from 'react'
import { useNavigate } from 'react-router-dom'
import type { OrderDetail, OrderPagination } from '../../models/order'
import { orderService } from '../../services/orderService'
import { Pagination } from '../../components/Pagination'
import { LoadingSpinner } from '../../components/LoadingSpinner'
import { ErrorMessage } from '../../components/ErrorMessage'
import { Header } from '../../components/Header'

export function PurchasesPage() {
  const navigate = useNavigate()
  const [orders, setOrders] = useState<OrderDetail[]>([])
  const [pagination, setPagination] = useState<OrderPagination | null>(null)
  const [page, setPage] = useState(1)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  const fetchOrders = useCallback(async () => {
    setLoading(true)
    setError('')
    try {
      const response = await orderService.getOrders({ page, per_page: 12 })
      setOrders(response.items)
      setPagination(response.pagination)
    } catch {
      setError('Failed to load your purchases. Please try again.')
    } finally {
      setLoading(false)
    }
  }, [page])

  useEffect(() => {
    fetchOrders()
  }, [fetchOrders])

  return (
    <div className="app">
      <Header />
      <main className="main-content">
        <div className="purchases-page">
          <div className="purchases-header">
            <h1 className="purchases-title">My Purchases</h1>
          </div>

          {loading && <LoadingSpinner message="Loading purchases..." />}
          {error && <ErrorMessage message={error} onRetry={fetchOrders} />}

          {!loading && !error && orders.length === 0 && (
            <div className="empty-state">
              <p>You haven't purchased any products yet.</p>
              <button className="empty-action" onClick={() => navigate('/products')}>
                Browse Products
              </button>
            </div>
          )}

          {!loading && !error && orders.length > 0 && (
            <>
              <div className="purchases-list">
                {orders.map((order) => (
                  <div className="purchase-card" key={order.id}>
                    <div className="purchase-card-main">
                      <h3 className="purchase-card-title">{order.product_title}</h3>
                      <span className={`product-card-location loc-${order.product_location.toLowerCase()}`}>
                        {order.product_location}
                      </span>
                    </div>
                    <div className="purchase-card-details">
                      <div className="purchase-meta">
                        <span className="purchase-label">Order</span>
                        <span className="purchase-value">#{order.id}</span>
                      </div>
                      <div className="purchase-meta">
                        <span className="purchase-label">Date</span>
                        <span className="purchase-value">
                          {new Date(order.created_at + 'Z').toLocaleString('en-GB', { timeZone: 'Asia/Amman' })}
                        </span>
                      </div>
                    </div>
                    <div className="purchase-card-footer">
                      <span className="purchase-price">${order.price_at_purchase}</span>
                      <button
                        className="purchase-view-btn"
                        onClick={() => navigate(`/receipt/${order.id}`)}
                      >
                        View Receipt
                      </button>
                    </div>
                  </div>
                ))}
              </div>
              {pagination && (
                <Pagination
                  currentPage={pagination.page}
                  totalPages={pagination.pages}
                  onPageChange={setPage}
                />
              )}
            </>
          )}
        </div>
      </main>
    </div>
  )
}