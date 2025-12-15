import { useEffect, useState } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { useTranslation } from 'react-i18next'
import { useTenant } from '../contexts/TenantContext'
import api from '../utils/api'
import toast from 'react-hot-toast'

const CheckoutPage = () => {
  const { t } = useTranslation()
  const { productId } = useParams()
  const navigate = useNavigate()
  const { currentTenant } = useTenant()
  
  const [product, setProduct] = useState(null)
  const [shippingClasses, setShippingClasses] = useState([])
  const [formData, setFormData] = useState({
    customer_name: '',
    customer_phone: '',
    customer_email: '',
    customer_address: '',
    quantity: 1,
    shipping_class_id: null
  })
  const [loading, setLoading] = useState(true)
  const [submitting, setSubmitting] = useState(false)

  useEffect(() => {
    loadData()
  }, [productId])

  const loadData = async () => {
    try {
      const [productRes, shippingRes] = await Promise.all([
        api.get(`/products/${productId}`),
        api.get('/shipping?active_only=true')
      ])
      
      setProduct(productRes.data)
      setShippingClasses(shippingRes.data)
      if (shippingRes.data.length > 0) {
        setFormData(prev => ({ ...prev, shipping_class_id: shippingRes.data[0].id }))
      }
      setLoading(false)
    } catch (error) {
      toast.error(t('common.error'))
      setLoading(false)
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setSubmitting(true)

    try {
      const orderData = {
        customer_name: formData.customer_name,
        customer_phone: formData.customer_phone,
        customer_email: formData.customer_email || null,
        customer_address: formData.customer_address,
        items: [{
          product_id: parseInt(productId),
          quantity: parseInt(formData.quantity)
        }],
        shipping_class_id: formData.shipping_class_id || null,
        payment_method: 'cod',
        fb_pixel_id: currentTenant?.facebook_pixel_id || null,
        fb_event_id: `order_${Date.now()}`
      }

      const response = await api.post('/orders', orderData)
      
      // Track Facebook Pixel (client-side)
      if (currentTenant?.enable_facebook_pixel && currentTenant?.facebook_pixel_id) {
        if (window.fbq) {
          window.fbq('track', 'Purchase', {
            value: parseFloat(response.data.total),
            currency: currentTenant.currency || 'BDT',
            content_ids: [productId],
            content_type: 'product'
          })
        }
      }

      navigate(`/order-confirmation/${response.data.id}`)
    } catch (error) {
      toast.error(error.response?.data?.detail || t('common.error'))
    } finally {
      setSubmitting(false)
    }
  }

  const calculateTotal = () => {
    if (!product) return 0
    const price = product.discount_price || product.price
    const subtotal = price * formData.quantity
    const shipping = shippingClasses.find(s => s.id === formData.shipping_class_id)?.cost || 0
    return subtotal + shipping
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
  const subtotal = displayPrice * formData.quantity
  const shippingCost = shippingClasses.find(s => s.id === formData.shipping_class_id)?.cost || 0
  const total = subtotal + shippingCost

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-2xl mx-auto px-4">
        <h1 className="text-2xl font-bold mb-6">{t('checkout.placeOrder')}</h1>

        <form onSubmit={handleSubmit} className="space-y-6">
          {/* Product Summary */}
          <div className="card">
            <div className="flex space-x-4">
              {product.images && product.images.length > 0 && (
                <img
                  src={product.images[0]}
                  alt={product.title}
                  className="w-24 h-24 object-cover rounded"
                />
              )}
              <div className="flex-1">
                <h3 className="font-semibold">{product.title}</h3>
                <p className="text-lg font-bold text-primary-600 mt-2">
                  ৳{displayPrice}
                </p>
              </div>
            </div>
          </div>

          {/* Customer Info */}
          <div className="card">
            <h2 className="text-xl font-semibold mb-4">Customer Information</h2>
            
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  {t('checkout.yourName')} <span className="text-red-500">*</span>
                </label>
                <input
                  type="text"
                  value={formData.customer_name}
                  onChange={(e) => setFormData({ ...formData, customer_name: e.target.value })}
                  className="input"
                  required
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  {t('checkout.mobileNumber')} <span className="text-red-500">*</span>
                </label>
                <input
                  type="tel"
                  value={formData.customer_phone}
                  onChange={(e) => setFormData({ ...formData, customer_phone: e.target.value })}
                  className="input"
                  required
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  {t('checkout.address')} <span className="text-red-500">*</span>
                </label>
                <textarea
                  value={formData.customer_address}
                  onChange={(e) => setFormData({ ...formData, customer_address: e.target.value })}
                  className="input"
                  rows={3}
                  required
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  {t('checkout.quantity')} <span className="text-red-500">*</span>
                </label>
                <input
                  type="number"
                  min="1"
                  max={product.stock_quantity || 999}
                  value={formData.quantity}
                  onChange={(e) => setFormData({ ...formData, quantity: parseInt(e.target.value) || 1 })}
                  className="input"
                  required
                />
              </div>
            </div>
          </div>

          {/* Shipping */}
          {shippingClasses.length > 0 && (
            <div className="card">
              <h2 className="text-xl font-semibold mb-4">{t('checkout.shipping')}</h2>
              
              <div className="space-y-2">
                {shippingClasses.map((shipping) => (
                  <label
                    key={shipping.id}
                    className="flex items-center p-4 border rounded-lg cursor-pointer hover:bg-gray-50"
                  >
                    <input
                      type="radio"
                      name="shipping"
                      value={shipping.id}
                      checked={formData.shipping_class_id === shipping.id}
                      onChange={(e) => setFormData({ ...formData, shipping_class_id: parseInt(e.target.value) })}
                      className="mr-3"
                    />
                    <div className="flex-1">
                      <div className="font-medium">{shipping.name_bn || shipping.name}</div>
                      <div className="text-sm text-gray-600">৳{shipping.cost}</div>
                    </div>
                  </label>
                ))}
              </div>
            </div>
          )}

          {/* Order Summary */}
          <div className="card">
            <h2 className="text-xl font-semibold mb-4">Order Summary</h2>
            
            <div className="space-y-2">
              <div className="flex justify-between">
                <span>{t('checkout.subtotal')}</span>
                <span>৳{subtotal}</span>
              </div>
              {shippingCost > 0 && (
                <div className="flex justify-between">
                  <span>{t('checkout.shipping')}</span>
                  <span>৳{shippingCost}</span>
                </div>
              )}
              <div className="flex justify-between text-lg font-bold pt-2 border-t">
                <span>{t('checkout.total')}</span>
                <span>৳{total}</span>
              </div>
            </div>
          </div>

          <button
            type="submit"
            disabled={submitting || !product.is_in_stock}
            className="btn btn-primary w-full touch-target text-lg py-4"
            style={{
              backgroundColor: currentTenant?.brand_color || '#3B82F6'
            }}
          >
            {submitting ? t('common.loading') : t('checkout.placeOrder')}
          </button>
        </form>
      </div>
    </div>
  )
}

export default CheckoutPage

