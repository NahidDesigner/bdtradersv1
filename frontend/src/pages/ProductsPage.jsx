import { useEffect, useState } from 'react'
import { useParams, Link } from 'react-router-dom'
import { useTranslation } from 'react-i18next'
import api from '../utils/api'
import toast from 'react-hot-toast'

const ProductsPage = () => {
  const { t } = useTranslation()
  const { storeId } = useParams()
  const [products, setProducts] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadProducts()
  }, [storeId])

  const loadProducts = async () => {
    try {
      // Note: In production, this would use tenant context from subdomain
      // For now, we'll need to pass storeId in query or header
      const response = await api.get('/products')
      setProducts(response.data)
      setLoading(false)
    } catch (error) {
      toast.error(t('common.error'))
      setLoading(false)
    }
  }

  const handleDelete = async (productId) => {
    if (!confirm('Are you sure?')) return
    
    try {
      await api.delete(`/products/${productId}`)
      toast.success('Product deleted')
      loadProducts()
    } catch (error) {
      toast.error(t('common.error'))
    }
  }

  if (loading) {
    return <div className="text-center py-12">{t('common.loading')}</div>
  }

  return (
    <div>
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-3xl font-bold">{t('product.products')}</h1>
        <Link
          to={`/app/stores/${storeId}/products/new`}
          className="btn btn-primary"
        >
          {t('product.addProduct')}
        </Link>
      </div>

      {products.length === 0 ? (
        <div className="card text-center py-12">
          <p className="text-lg text-gray-600 mb-4">{t('product.noProducts')}</p>
          <Link
            to={`/app/stores/${storeId}/products/new`}
            className="btn btn-primary"
          >
            {t('product.addProduct')}
          </Link>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {products.map((product) => (
            <div key={product.id} className="card">
              {product.images && product.images.length > 0 && (
                <img
                  src={product.images[0]}
                  alt={product.title}
                  className="w-full h-48 object-cover rounded-lg mb-4"
                />
              )}
              <h3 className="text-xl font-semibold mb-2">{product.title}</h3>
              <div className="flex items-center justify-between mb-4">
                <div>
                  {product.discount_price ? (
                    <div>
                      <span className="text-2xl font-bold text-primary-600">
                        ৳{product.discount_price}
                      </span>
                      <span className="text-sm text-gray-500 line-through ml-2">
                        ৳{product.price}
                      </span>
                    </div>
                  ) : (
                    <span className="text-2xl font-bold text-primary-600">
                      ৳{product.price}
                    </span>
                  )}
                </div>
                <span className={`px-2 py-1 rounded text-sm ${
                  product.is_in_stock ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
                }`}>
                  {product.is_in_stock ? t('product.inStock') : t('product.outOfStock')}
                </span>
              </div>
              <div className="flex space-x-2">
                <Link
                  to={`/app/stores/${storeId}/products/${product.id}/edit`}
                  className="btn btn-secondary flex-1 text-sm"
                >
                  {t('common.edit')}
                </Link>
                <button
                  onClick={() => handleDelete(product.id)}
                  className="btn btn-secondary flex-1 text-sm text-red-600"
                >
                  {t('common.delete')}
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}

export default ProductsPage

