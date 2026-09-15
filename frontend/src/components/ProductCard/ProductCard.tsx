import { useNavigate } from 'react-router-dom'
import type { Product } from '../../models/product'

interface ProductCardProps {
  product: Product
}

export function ProductCard({ product }: ProductCardProps) {
  const navigate = useNavigate()

  return (
    <div className="product-card">
      <div className="product-card-header">
        <h3 className="product-card-title">{product.title}</h3>
        <span className={`product-card-location loc-${product.location.toLowerCase()}`}>
          {product.location}
        </span>
      </div>
      {product.description && (
        <p className="product-card-description">{product.description}</p>
      )}
      <div className="product-card-footer">
        <span className="product-card-price">${product.price}</span>
        <button
          className="product-card-btn"
          onClick={() => navigate(`/products/${product.id}`)}
        >
          View Details
        </button>
      </div>
    </div>
  )
}
