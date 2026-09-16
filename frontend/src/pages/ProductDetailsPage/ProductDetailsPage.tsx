import { useState, useEffect, useCallback } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import type { Product } from '../../models/product'
import { productService } from '../../services/productService'
import { orderService } from '../../services/orderService'
import { LoadingSpinner } from '../../components/LoadingSpinner'
import { ErrorMessage } from '../../components/ErrorMessage'
import { Header } from '../../components/Header'

export function ProductDetailsPage() {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()
  const [product, setProduct] = useState<Product | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [purchasing, setPurchasing] = useState(false)
  const [purchaseError, setPurchaseError] = useState('')

  const fetchProduct = useCallback(async () => {
    if (!id) return
    setLoading(true)
    setError('')
    try {
      const data = await productService.getProductById(Number(id))
      setProduct(data)
    } catch (err: unknown) {
      if (err && typeof err === 'object' && 'response' in err) {
        const axiosErr = err as { response?: { status?: number } }
        if (axiosErr.response?.status === 404) {
          setError('Product not found.')
          return
        }
      }
      setError('Failed to load product details. Please try again.')
    } finally {
      setLoading(false)
    }
  }, [id])

  useEffect(() => {
    fetchProduct()
  }, [fetchProduct])

  const handlePurchase = async () => {
    if (!product || purchasing) return
    setPurchasing(true)
    setPurchaseError('')
    try {
      const order = await orderService.createOrder({ product_id: product.id })
      navigate(`/receipt/${order.id}`)
    } catch (err: unknown) {
      if (err && typeof err === 'object' && 'response' in err) {
        const axiosErr = err as { response?: { status?: number; data?: { error?: { message?: string } } } }
        if (axiosErr.response?.status === 404) {
          setPurchaseError('Product not found.')
          return
        }
        if (axiosErr.response?.status === 409) {
          setPurchaseError('You have already purchased this product.')
          navigate('/purchases')
          return
        }
        if (axiosErr.response?.data?.error?.message) {
          setPurchaseError(axiosErr.response.data.error.message)
          return
        }
      }
      setPurchaseError('Failed to complete purchase. Please try again.')
    } finally {
      setPurchasing(false)
    }
  }

  return (
    <div className="app">
      <Header />
      <main className="main-content">
        {loading && <LoadingSpinner message="Loading product..." />}
        {error && <ErrorMessage message={error} onRetry={fetchProduct} />}

        {!loading && !error && product && (
          <div className="product-details">
            <button className="back-btn" onClick={() => navigate('/products')}>
              Back to Products
            </button>
            <div className="product-details-card">
              <div className="product-details-header">
                <h1 className="product-details-title">{product.title}</h1>
                <span className={`product-card-location loc-${product.location.toLowerCase()}`}>
                  {product.location}
                </span>
              </div>
              {product.description && (
                <p className="product-details-description">{product.description}</p>
              )}
              <div className="product-details-price-row">
                <span className="product-details-price">${product.price}</span>
                <button
                  className="buy-btn"
                  onClick={handlePurchase}
                  disabled={purchasing}
                >
                  {purchasing ? 'Processing...' : 'Buy Now'}
                </button>
              </div>
              {purchaseError && (
                <div className="purchase-error">{purchaseError}</div>
              )}
            </div>
          </div>
        )}
      </main>
    </div>
  )
}
