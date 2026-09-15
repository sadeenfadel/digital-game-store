import { useState, useEffect, useCallback } from 'react'
import type { Product, Pagination as PaginationType } from '../../models/product'
import type { Location } from '../../models/product'
import { productService } from '../../services/productService'
import { ProductCard } from '../../components/ProductCard'
import { Pagination } from '../../components/Pagination'
import { LocationFilter } from '../../components/LocationFilter'
import { LoadingSpinner } from '../../components/LoadingSpinner'
import { ErrorMessage } from '../../components/ErrorMessage'
import { Header } from '../../components/Header'

type FilterValue = Location | 'ALL'

export function ProductsPage() {
  const [products, setProducts] = useState<Product[]>([])
  const [pagination, setPagination] = useState<PaginationType | null>(null)
  const [page, setPage] = useState(1)
  const [location, setLocation] = useState<FilterValue>('ALL')
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  const fetchProducts = useCallback(async () => {
    setLoading(true)
    setError('')
    try {
      const params: { page: number; per_page: number; location?: string } = {
        page,
        per_page: 12,
      }
      if (location !== 'ALL') {
        params.location = location
      }
      const response = await productService.getProducts(params)
      setProducts(response.items)
      setPagination(response.pagination)
    } catch {
      setError('Failed to load products. Please try again.')
    } finally {
      setLoading(false)
    }
  }, [page, location])

  useEffect(() => {
    fetchProducts()
  }, [fetchProducts])

  const handleLocationChange = (newLocation: FilterValue) => {
    setLocation(newLocation)
    setPage(1)
  }

  const handlePageChange = (newPage: number) => {
    setPage(newPage)
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }

  return (
    <div className="app">
      <Header />
      <main className="main-content">
        <div className="products-page">
          <div className="products-header">
            <h1 className="products-title">Products</h1>
            <LocationFilter value={location} onChange={handleLocationChange} />
          </div>

          {loading && <LoadingSpinner message="Loading products..." />}
          {error && <ErrorMessage message={error} onRetry={fetchProducts} />}

          {!loading && !error && products.length === 0 && (
            <div className="empty-state">
              <p>No products found for this location.</p>
            </div>
          )}

          {!loading && !error && products.length > 0 && (
            <>
              <div className="products-grid">
                {products.map((product) => (
                  <ProductCard key={product.id} product={product} />
                ))}
              </div>
              {pagination && (
                <Pagination
                  currentPage={pagination.page}
                  totalPages={pagination.pages}
                  onPageChange={handlePageChange}
                />
              )}
            </>
          )}
        </div>
      </main>
    </div>
  )
}
