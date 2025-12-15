import { useEffect, useState } from 'react'
import { useTranslation } from 'react-i18next'
import { useTenant } from '../contexts/TenantContext'
import { Link } from 'react-router-dom'
import api from '../utils/api'
import toast from 'react-hot-toast'

const DashboardPage = () => {
  const { t } = useTranslation()
  const { tenants, loadUserTenants } = useTenant()
  const [stats, setStats] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadUserTenants()
  }, [])

  // Load stats for first tenant (in production, show aggregated or selected tenant)
  useEffect(() => {
    if (tenants.length > 0) {
      loadStats(tenants[0].id)
    } else {
      setLoading(false)
    }
  }, [tenants])

  const loadStats = async (tenantId) => {
    try {
      // Note: This would need tenant context in request
      // For now, showing placeholder
      setStats({
        totalOrders: 0,
        totalSales: 0,
        pendingOrders: 0,
        todayOrders: 0
      })
      setLoading(false)
    } catch (error) {
      toast.error(t('common.error'))
      setLoading(false)
    }
  }

  if (loading) {
    return <div className="text-center py-12">{t('common.loading')}</div>
  }

  if (tenants.length === 0) {
    return (
      <div className="text-center py-12">
        <p className="text-lg text-gray-600 mb-4">{t('store.noStores')}</p>
        <Link to="/app/stores" className="btn btn-primary">
          {t('store.createFirstStore')}
        </Link>
      </div>
    )
  }

  return (
    <div>
      <h1 className="text-3xl font-bold mb-8">{t('analytics.dashboard')}</h1>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <div className="card">
          <h3 className="text-sm font-medium text-gray-500 mb-2">
            {t('analytics.totalOrders')}
          </h3>
          <p className="text-3xl font-bold text-gray-900">
            {stats?.totalOrders || 0}
          </p>
        </div>

        <div className="card">
          <h3 className="text-sm font-medium text-gray-500 mb-2">
            {t('analytics.totalSales')}
          </h3>
          <p className="text-3xl font-bold text-gray-900">
            ৳{stats?.totalSales || 0}
          </p>
        </div>

        <div className="card">
          <h3 className="text-sm font-medium text-gray-500 mb-2">
            {t('analytics.pendingOrders')}
          </h3>
          <p className="text-3xl font-bold text-yellow-600">
            {stats?.pendingOrders || 0}
          </p>
        </div>

        <div className="card">
          <h3 className="text-sm font-medium text-gray-500 mb-2">
            {t('analytics.todayOrders')}
          </h3>
          <p className="text-3xl font-bold text-primary-600">
            {stats?.todayOrders || 0}
          </p>
        </div>
      </div>

      {/* Quick Actions */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <Link
          to="/app/stores"
          className="card hover:shadow-md transition-shadow"
        >
          <h3 className="text-lg font-semibold mb-2">🏪 {t('store.myStores')}</h3>
          <p className="text-sm text-gray-600">
            {tenants.length} {tenants.length === 1 ? 'store' : 'stores'}
          </p>
        </Link>

        <Link
          to={`/app/stores/${tenants[0]?.id}/products`}
          className="card hover:shadow-md transition-shadow"
        >
          <h3 className="text-lg font-semibold mb-2">📦 {t('product.products')}</h3>
          <p className="text-sm text-gray-600">Manage products</p>
        </Link>

        <Link
          to={`/app/stores/${tenants[0]?.id}/orders`}
          className="card hover:shadow-md transition-shadow"
        >
          <h3 className="text-lg font-semibold mb-2">📋 {t('order.orders')}</h3>
          <p className="text-sm text-gray-600">View orders</p>
        </Link>
      </div>
    </div>
  )
}

export default DashboardPage

