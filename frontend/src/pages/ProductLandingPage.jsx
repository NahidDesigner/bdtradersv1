import { useEffect, useState } from 'react'
import { useParams, Link } from 'react-router-dom'
import { useTranslation } from 'react-i18next'
import { useTenant } from '../contexts/TenantContext'
import api from '../utils/api'

const ProductLandingPage = () => {
  const { t } = useTranslation()
  const { slug } = useParams()
  const { currentTenant } = useTenant()
  const [product, setProduct] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadProduct()
  }, [slug])

  const loadProduct = async () => {
    try {
      const response = await api.get(`/products/slug/${slug}`)
      setProduct(response.data)
      setLoading(false)
    } catch (error) {
      setLoading(false)
    }
  }

  if (loading) {
    return <div className="min-h-screen flex items-center justify-center">
      <div>{t('common.loading')}</div>
    </div>
  }

  if (!product) {
    return <div className="min-h-screen flex items-center justify-center">
      <div>Product not found</div>
    </div>
  }

  const displayPrice = product.discount_price || product.price
  const originalPrice = product.discount_price ? product.price : null

  return (
    <div className="min-h-screen bg-white">
      {/* Product Images */}
      <div className="w-full h-96 bg-gray-100 flex items-center justify-center">
        {product.images && product.images.length > 0 ? (
          <img
            src={product.images[0]}
            alt={product.title}
            className="w-full h-full object-cover"
          />
        ) : (
          <div className="text-gray-400">No image</div>
        )}
      </div>

      {/* Product Info */}
      <div className="max-w-4xl mx-auto px-4 py-8">
        <h1 className="text-3xl font-bold mb-4">{product.title}</h1>
        
        {product.description && (
          <div className="prose mb-6" dangerouslySetInnerHTML={{ __html: product.description }} />
        )}

        <div className="border-t border-gray-200 pt-6">
          <div className="flex items-center space-x-4 mb-6">
            {originalPrice && (
              <span className="text-xl text-gray-500 line-through">
                ৳{originalPrice}
              </span>
            )}
            <span className="text-4xl font-bold text-primary-600">
              ৳{displayPrice}
            </span>
          </div>

          <div className="mb-6">
            <span className={`px-3 py-1 rounded-full text-sm font-medium ${
              product.is_in_stock
                ? 'bg-green-100 text-green-800'
                : 'bg-red-100 text-red-800'
            }`}>
              {product.is_in_stock ? t('product.inStock') : t('product.outOfStock')}
            </span>
          </div>

          <Link
            to={`/checkout/${product.id}`}
            className="btn btn-primary w-full touch-target text-lg py-4"
            style={{
              backgroundColor: currentTenant?.brand_color || '#3B82F6'
            }}
          >
            {t('checkout.placeOrder')}
          </Link>
        </div>
      </div>
    </div>
  )
}

export default ProductLandingPage

