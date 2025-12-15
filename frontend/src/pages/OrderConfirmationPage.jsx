import { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'
import { useTranslation } from 'react-i18next'
import api from '../utils/api'

const OrderConfirmationPage = () => {
  const { t } = useTranslation()
  const { orderId } = useParams()
  const [order, setOrder] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadOrder()
  }, [orderId])

  const loadOrder = async () => {
    try {
      const response = await api.get(`/orders/${orderId}`)
      setOrder(response.data)
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

  if (!order) {
    return <div className="min-h-screen flex items-center justify-center">
      <div>Order not found</div>
    </div>
  }

  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center px-4 py-12">
      <div className="max-w-md w-full">
        <div className="card text-center">
          <div className="text-6xl mb-4">✅</div>
          <h1 className="text-2xl font-bold mb-4">
            {t('order.orderReceived')}
          </h1>
          <p className="text-gray-600 mb-6">
            {t('order.contactSoon')}
          </p>

          <div className="text-left space-y-2 mb-6 p-4 bg-gray-50 rounded-lg">
            <div>
              <span className="text-sm text-gray-500">{t('order.orderNumber')}:</span>
              <span className="ml-2 font-semibold">{order.order_number}</span>
            </div>
            <div>
              <span className="text-sm text-gray-500">{t('order.total')}:</span>
              <span className="ml-2 font-semibold text-lg">৳{order.total}</span>
            </div>
          </div>

          <p className="text-sm text-gray-500">
            We will contact you at {order.customer_phone} soon.
          </p>
        </div>
      </div>
    </div>
  )
}

export default OrderConfirmationPage

