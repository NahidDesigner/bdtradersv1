import { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'
import { useTranslation } from 'react-i18next'
import api from '../utils/api'
import toast from 'react-hot-toast'

const OrdersPage = () => {
  const { t } = useTranslation()
  const { storeId } = useParams()
  const [orders, setOrders] = useState([])
  const [loading, setLoading] = useState(true)
  const [statusFilter, setStatusFilter] = useState('')

  useEffect(() => {
    loadOrders()
  }, [storeId, statusFilter])

  const loadOrders = async () => {
    try {
      const params = statusFilter ? { status_filter: statusFilter } : {}
      const response = await api.get('/orders', { params })
      setOrders(response.data)
      setLoading(false)
    } catch (error) {
      toast.error(t('common.error'))
      setLoading(false)
    }
  }

  const updateOrderStatus = async (orderId, newStatus) => {
    try {
      await api.put(`/orders/${orderId}`, { status: newStatus })
      toast.success('Order updated')
      loadOrders()
    } catch (error) {
      toast.error(t('common.error'))
    }
  }

  const getStatusColor = (status) => {
    const colors = {
      pending: 'bg-yellow-100 text-yellow-800',
      confirmed: 'bg-blue-100 text-blue-800',
      shipped: 'bg-purple-100 text-purple-800',
      delivered: 'bg-green-100 text-green-800',
      cancelled: 'bg-red-100 text-red-800'
    }
    return colors[status] || 'bg-gray-100 text-gray-800'
  }

  if (loading) {
    return <div className="text-center py-12">{t('common.loading')}</div>
  }

  return (
    <div>
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-3xl font-bold">{t('order.orders')}</h1>
        <select
          value={statusFilter}
          onChange={(e) => setStatusFilter(e.target.value)}
          className="input w-auto"
        >
          <option value="">All Status</option>
          <option value="pending">{t('order.pending')}</option>
          <option value="confirmed">{t('order.confirmed')}</option>
          <option value="shipped">{t('order.shipped')}</option>
          <option value="delivered">{t('order.delivered')}</option>
          <option value="cancelled">{t('order.cancelled')}</option>
        </select>
      </div>

      {orders.length === 0 ? (
        <div className="card text-center py-12">
          <p className="text-lg text-gray-600">{t('order.noOrders')}</p>
        </div>
      ) : (
        <div className="space-y-4">
          {orders.map((order) => (
            <div key={order.id} className="card">
              <div className="flex justify-between items-start mb-4">
                <div>
                  <h3 className="text-lg font-semibold">{order.order_number}</h3>
                  <p className="text-sm text-gray-600">
                    {new Date(order.created_at).toLocaleDateString('bn-BD')}
                  </p>
                </div>
                <span className={`px-3 py-1 rounded-full text-sm font-medium ${getStatusColor(order.status)}`}>
                  {t(`order.${order.status}`)}
                </span>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
                <div>
                  <p className="text-sm text-gray-500">{t('order.customerName')}</p>
                  <p className="font-medium">{order.customer_name}</p>
                </div>
                <div>
                  <p className="text-sm text-gray-500">{t('order.customerPhone')}</p>
                  <p className="font-medium">{order.customer_phone}</p>
                </div>
                <div>
                  <p className="text-sm text-gray-500">{t('order.total')}</p>
                  <p className="font-bold text-lg">৳{order.total}</p>
                </div>
              </div>

              <div className="mb-4">
                <p className="text-sm text-gray-500 mb-1">{t('order.customerAddress')}</p>
                <p className="text-sm">{order.customer_address}</p>
              </div>

              {order.items && order.items.length > 0 && (
                <div className="mb-4">
                  <p className="text-sm font-medium mb-2">Items:</p>
                  <div className="space-y-1">
                    {order.items.map((item, idx) => (
                      <div key={idx} className="text-sm text-gray-600">
                        {item.product_title} × {item.quantity} = ৳{item.subtotal}
                      </div>
                    ))}
                  </div>
                </div>
              )}

              <div className="flex space-x-2">
                <select
                  value={order.status}
                  onChange={(e) => updateOrderStatus(order.id, e.target.value)}
                  className="input flex-1 text-sm"
                >
                  <option value="pending">{t('order.pending')}</option>
                  <option value="confirmed">{t('order.confirmed')}</option>
                  <option value="shipped">{t('order.shipped')}</option>
                  <option value="delivered">{t('order.delivered')}</option>
                  <option value="cancelled">{t('order.cancelled')}</option>
                </select>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}

export default OrdersPage

