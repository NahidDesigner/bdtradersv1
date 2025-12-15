import { useEffect, useState } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { useTranslation } from 'react-i18next'
import api from '../utils/api'
import toast from 'react-hot-toast'

const ProductFormPage = () => {
  const { t } = useTranslation()
  const { storeId, productId } = useParams()
  const navigate = useNavigate()
  const isEdit = !!productId
  
  const [formData, setFormData] = useState({
    title: '',
    title_bn: '',
    description: '',
    description_bn: '',
    price: '',
    discount_price: '',
    stock_quantity: 0,
    is_in_stock: true,
    track_inventory: true,
    images: [],
    is_published: true,
    is_featured: false
  })
  const [loading, setLoading] = useState(false)
  const [saving, setSaving] = useState(false)

  useEffect(() => {
    if (isEdit) {
      loadProduct()
    }
  }, [productId])

  const loadProduct = async () => {
    try {
      const response = await api.get(`/products/${productId}`)
      const product = response.data
      setFormData({
        title: product.title || '',
        title_bn: product.title_bn || '',
        description: product.description || '',
        description_bn: product.description_bn || '',
        price: product.price || '',
        discount_price: product.discount_price || '',
        stock_quantity: product.stock_quantity || 0,
        is_in_stock: product.is_in_stock,
        track_inventory: product.track_inventory,
        images: product.images || [],
        is_published: product.is_published,
        is_featured: product.is_featured
      })
      setLoading(false)
    } catch (error) {
      toast.error(t('common.error'))
      navigate(`/app/stores/${storeId}/products`)
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setSaving(true)
    
    try {
      const data = {
        ...formData,
        price: parseFloat(formData.price),
        discount_price: formData.discount_price ? parseFloat(formData.discount_price) : null,
        stock_quantity: parseInt(formData.stock_quantity)
      }
      
      if (isEdit) {
        await api.put(`/products/${productId}`, data)
        toast.success('Product updated')
      } else {
        await api.post('/products', data)
        toast.success('Product created')
      }
      
      navigate(`/app/stores/${storeId}/products`)
    } catch (error) {
      toast.error(error.response?.data?.detail || t('common.error'))
    } finally {
      setSaving(false)
    }
  }

  if (loading) {
    return <div className="text-center py-12">{t('common.loading')}</div>
  }

  return (
    <div>
      <div className="flex items-center mb-8">
        <button
          onClick={() => navigate(`/app/stores/${storeId}/products`)}
          className="mr-4 text-gray-600 hover:text-gray-900"
        >
          ← {t('common.back')}
        </button>
        <h1 className="text-3xl font-bold">
          {isEdit ? t('product.editProduct') : t('product.addProduct')}
        </h1>
      </div>

      <form onSubmit={handleSubmit} className="space-y-6">
        <div className="card">
          <h2 className="text-xl font-semibold mb-4">Basic Information</h2>
          
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                {t('product.title')} <span className="text-red-500">*</span>
              </label>
              <input
                type="text"
                value={formData.title}
                onChange={(e) => setFormData({ ...formData, title: e.target.value })}
                className="input"
                required
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                {t('product.title')} (বাংলা)
              </label>
              <input
                type="text"
                value={formData.title_bn}
                onChange={(e) => setFormData({ ...formData, title_bn: e.target.value })}
                className="input"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                {t('product.description')}
              </label>
              <textarea
                value={formData.description}
                onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                className="input"
                rows={4}
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                {t('product.description')} (বাংলা)
              </label>
              <textarea
                value={formData.description_bn}
                onChange={(e) => setFormData({ ...formData, description_bn: e.target.value })}
                className="input"
                rows={4}
              />
            </div>
          </div>
        </div>

        <div className="card">
          <h2 className="text-xl font-semibold mb-4">Pricing & Inventory</h2>
          
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                {t('product.price')} <span className="text-red-500">*</span>
              </label>
              <input
                type="number"
                step="0.01"
                value={formData.price}
                onChange={(e) => setFormData({ ...formData, price: e.target.value })}
                className="input"
                required
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                {t('product.discountPrice')}
              </label>
              <input
                type="number"
                step="0.01"
                value={formData.discount_price}
                onChange={(e) => setFormData({ ...formData, discount_price: e.target.value })}
                className="input"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                {t('product.stock')}
              </label>
              <input
                type="number"
                value={formData.stock_quantity}
                onChange={(e) => setFormData({ ...formData, stock_quantity: e.target.value })}
                className="input"
                min="0"
              />
            </div>

            <div className="flex items-center pt-8">
              <input
                type="checkbox"
                id="track_inventory"
                checked={formData.track_inventory}
                onChange={(e) => setFormData({ ...formData, track_inventory: e.target.checked })}
                className="mr-2"
              />
              <label htmlFor="track_inventory" className="text-sm font-medium text-gray-700">
                Track Inventory
              </label>
            </div>
          </div>
        </div>

        <div className="card">
          <h2 className="text-xl font-semibold mb-4">Status</h2>
          
          <div className="space-y-2">
            <div className="flex items-center">
              <input
                type="checkbox"
                id="is_published"
                checked={formData.is_published}
                onChange={(e) => setFormData({ ...formData, is_published: e.target.checked })}
                className="mr-2"
              />
              <label htmlFor="is_published" className="text-sm font-medium text-gray-700">
                {t('product.published')}
              </label>
            </div>

            <div className="flex items-center">
              <input
                type="checkbox"
                id="is_featured"
                checked={formData.is_featured}
                onChange={(e) => setFormData({ ...formData, is_featured: e.target.checked })}
                className="mr-2"
              />
              <label htmlFor="is_featured" className="text-sm font-medium text-gray-700">
                Featured Product
              </label>
            </div>
          </div>
        </div>

        <div className="flex space-x-4">
          <button
            type="submit"
            disabled={saving}
            className="btn btn-primary flex-1"
          >
            {saving ? t('common.loading') : t('common.save')}
          </button>
          <button
            type="button"
            onClick={() => navigate(`/app/stores/${storeId}/products`)}
            className="btn btn-secondary flex-1"
          >
            {t('common.cancel')}
          </button>
        </div>
      </form>
    </div>
  )
}

export default ProductFormPage

