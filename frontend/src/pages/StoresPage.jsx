import { useEffect, useState } from 'react'
import { useTranslation } from 'react-i18next'
import { useTenant } from '../contexts/TenantContext'
import { Link } from 'react-router-dom'
import toast from 'react-hot-toast'
import api from '../utils/api'

const StoresPage = () => {
  const { t } = useTranslation()
  const { tenants, loadUserTenants, createTenant } = useTenant()
  const [showCreateForm, setShowCreateForm] = useState(false)
  const [formData, setFormData] = useState({
    name: '',
    slug: '',
    brand_color: '#3B82F6',
    currency: 'BDT',
    default_language: 'bn'
  })
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    loadUserTenants()
  }, [])

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    
    const result = await createTenant(formData)
    setLoading(false)
    
    if (result.success) {
      toast.success('স্টোর তৈরি হয়েছে')
      setShowCreateForm(false)
      setFormData({
        name: '',
        slug: '',
        brand_color: '#3B82F6',
        currency: 'BDT',
        default_language: 'bn'
      })
    } else {
      toast.error(result.error)
    }
  }

  const generateSlug = (name) => {
    return name
      .toLowerCase()
      .replace(/[^a-z0-9]+/g, '-')
      .replace(/^-+|-+$/g, '')
  }

  return (
    <div>
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-3xl font-bold">{t('store.myStores')}</h1>
        <button
          onClick={() => setShowCreateForm(!showCreateForm)}
          className="btn btn-primary"
        >
          {t('store.createStore')}
        </button>
      </div>

      {showCreateForm && (
        <div className="card mb-8">
          <h2 className="text-xl font-semibold mb-4">{t('store.createStore')}</h2>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                {t('store.storeName')} <span className="text-red-500">*</span>
              </label>
              <input
                type="text"
                value={formData.name}
                onChange={(e) => {
                  setFormData({
                    ...formData,
                    name: e.target.value,
                    slug: generateSlug(e.target.value)
                  })
                }}
                className="input"
                required
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                {t('store.storeSlug')} <span className="text-red-500">*</span>
              </label>
              <input
                type="text"
                value={formData.slug}
                onChange={(e) => setFormData({ ...formData, slug: e.target.value })}
                className="input"
                pattern="[a-z0-9-]+"
                required
              />
              <p className="text-xs text-gray-500 mt-1">
                Store URL: {formData.slug || 'slug'}.yourdomain.com
              </p>
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  {t('store.brandColor')}
                </label>
                <input
                  type="color"
                  value={formData.brand_color}
                  onChange={(e) => setFormData({ ...formData, brand_color: e.target.value })}
                  className="w-full h-10 rounded"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  {t('store.currency')}
                </label>
                <select
                  value={formData.currency}
                  onChange={(e) => setFormData({ ...formData, currency: e.target.value })}
                  className="input"
                >
                  <option value="BDT">BDT (৳)</option>
                  <option value="USD">USD ($)</option>
                </select>
              </div>
            </div>

            <div className="flex space-x-4">
              <button
                type="submit"
                disabled={loading}
                className="btn btn-primary flex-1"
              >
                {loading ? t('common.loading') : t('common.save')}
              </button>
              <button
                type="button"
                onClick={() => setShowCreateForm(false)}
                className="btn btn-secondary flex-1"
              >
                {t('common.cancel')}
              </button>
            </div>
          </form>
        </div>
      )}

      {tenants.length === 0 ? (
        <div className="card text-center py-12">
          <p className="text-lg text-gray-600 mb-4">{t('store.noStores')}</p>
          <button
            onClick={() => setShowCreateForm(true)}
            className="btn btn-primary"
          >
            {t('store.createFirstStore')}
          </button>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {tenants.map((tenant) => (
            <Link
              key={tenant.id}
              to={`/app/stores/${tenant.id}/settings`}
              className="card hover:shadow-lg transition-shadow"
            >
              <div
                className="h-32 rounded-lg mb-4"
                style={{ backgroundColor: tenant.brand_color }}
              />
              <h3 className="text-xl font-semibold mb-2">{tenant.name}</h3>
              <p className="text-sm text-gray-600 mb-4">
                {tenant.slug}.yourdomain.com
              </p>
              <div className="flex items-center justify-between text-sm">
                <span className="text-gray-500">{tenant.currency}</span>
                <span className={`px-2 py-1 rounded ${
                  tenant.is_active ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'
                }`}>
                  {tenant.is_active ? 'Active' : 'Inactive'}
                </span>
              </div>
            </Link>
          ))}
        </div>
      )}
    </div>
  )
}

export default StoresPage

