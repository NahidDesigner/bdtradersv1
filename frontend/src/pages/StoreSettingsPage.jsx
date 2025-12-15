import { useEffect, useState } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { useTranslation } from 'react-i18next'
import { useTenant } from '../contexts/TenantContext'
import toast from 'react-hot-toast'
import api from '../utils/api'

const StoreSettingsPage = () => {
  const { t } = useTranslation()
  const { storeId } = useParams()
  const navigate = useNavigate()
  const { updateTenant } = useTenant()
  const [tenant, setTenant] = useState(null)
  const [formData, setFormData] = useState({})
  const [loading, setLoading] = useState(true)
  const [saving, setSaving] = useState(false)

  useEffect(() => {
    loadTenant()
  }, [storeId])

  const loadTenant = async () => {
    try {
      const response = await api.get(`/tenants/${storeId}`)
      setTenant(response.data)
      setFormData({
        name: response.data.name,
        brand_color: response.data.brand_color,
        currency: response.data.currency,
        default_language: response.data.default_language,
        whatsapp_number: response.data.whatsapp_number || '',
        support_phone: response.data.support_phone || '',
        enable_cod: response.data.enable_cod,
        enable_facebook_pixel: response.data.enable_facebook_pixel,
        facebook_pixel_id: response.data.facebook_pixel_id || '',
        email_notifications: response.data.email_notifications,
        whatsapp_notifications: response.data.whatsapp_notifications,
        notification_email: response.data.notification_email || '',
        notification_whatsapp: response.data.notification_whatsapp || ''
      })
      setLoading(false)
    } catch (error) {
      toast.error(t('common.error'))
      navigate('/app/stores')
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setSaving(true)
    
    const result = await updateTenant(parseInt(storeId), formData)
    setSaving(false)
    
    if (result.success) {
      toast.success(t('common.success'))
      setTenant(result.data)
    } else {
      toast.error(result.error)
    }
  }

  if (loading) {
    return <div className="text-center py-12">{t('common.loading')}</div>
  }

  return (
    <div>
      <div className="flex items-center mb-8">
        <button
          onClick={() => navigate('/app/stores')}
          className="mr-4 text-gray-600 hover:text-gray-900"
        >
          ← {t('common.back')}
        </button>
        <h1 className="text-3xl font-bold">{tenant?.name} - {t('store.settings')}</h1>
      </div>

      <form onSubmit={handleSubmit} className="space-y-6">
        <div className="card">
          <h2 className="text-xl font-semibold mb-4">General Settings</h2>
          
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                {t('store.storeName')}
              </label>
              <input
                type="text"
                value={formData.name}
                onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                className="input"
                required
              />
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
          </div>
        </div>

        <div className="card">
          <h2 className="text-xl font-semibold mb-4">Contact Information</h2>
          
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                WhatsApp Number
              </label>
              <input
                type="tel"
                value={formData.whatsapp_number}
                onChange={(e) => setFormData({ ...formData, whatsapp_number: e.target.value })}
                className="input"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Support Phone
              </label>
              <input
                type="tel"
                value={formData.support_phone}
                onChange={(e) => setFormData({ ...formData, support_phone: e.target.value })}
                className="input"
              />
            </div>
          </div>
        </div>

        <div className="card">
          <h2 className="text-xl font-semibold mb-4">Payment Settings</h2>
          
          <div className="flex items-center">
            <input
              type="checkbox"
              id="enable_cod"
              checked={formData.enable_cod}
              onChange={(e) => setFormData({ ...formData, enable_cod: e.target.checked })}
              className="mr-2"
            />
            <label htmlFor="enable_cod" className="text-sm font-medium text-gray-700">
              Enable Cash on Delivery
            </label>
          </div>
        </div>

        <div className="card">
          <h2 className="text-xl font-semibold mb-4">Facebook Pixel</h2>
          
          <div className="space-y-4">
            <div className="flex items-center">
              <input
                type="checkbox"
                id="enable_facebook_pixel"
                checked={formData.enable_facebook_pixel}
                onChange={(e) => setFormData({ ...formData, enable_facebook_pixel: e.target.checked })}
                className="mr-2"
              />
              <label htmlFor="enable_facebook_pixel" className="text-sm font-medium text-gray-700">
                Enable Facebook Pixel
              </label>
            </div>

            {formData.enable_facebook_pixel && (
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Facebook Pixel ID
                </label>
                <input
                  type="text"
                  value={formData.facebook_pixel_id}
                  onChange={(e) => setFormData({ ...formData, facebook_pixel_id: e.target.value })}
                  className="input"
                />
              </div>
            )}
          </div>
        </div>

        <div className="card">
          <h2 className="text-xl font-semibold mb-4">Notifications</h2>
          
          <div className="space-y-4">
            <div className="flex items-center">
              <input
                type="checkbox"
                id="email_notifications"
                checked={formData.email_notifications}
                onChange={(e) => setFormData({ ...formData, email_notifications: e.target.checked })}
                className="mr-2"
              />
              <label htmlFor="email_notifications" className="text-sm font-medium text-gray-700">
                Email Notifications
              </label>
            </div>

            {formData.email_notifications && (
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Notification Email
                </label>
                <input
                  type="email"
                  value={formData.notification_email}
                  onChange={(e) => setFormData({ ...formData, notification_email: e.target.value })}
                  className="input"
                />
              </div>
            )}

            <div className="flex items-center">
              <input
                type="checkbox"
                id="whatsapp_notifications"
                checked={formData.whatsapp_notifications}
                onChange={(e) => setFormData({ ...formData, whatsapp_notifications: e.target.checked })}
                className="mr-2"
              />
              <label htmlFor="whatsapp_notifications" className="text-sm font-medium text-gray-700">
                WhatsApp Notifications
              </label>
            </div>

            {formData.whatsapp_notifications && (
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Notification WhatsApp
                </label>
                <input
                  type="tel"
                  value={formData.notification_whatsapp}
                  onChange={(e) => setFormData({ ...formData, notification_whatsapp: e.target.value })}
                  className="input"
                />
              </div>
            )}
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
            onClick={() => navigate('/app/stores')}
            className="btn btn-secondary flex-1"
          >
            {t('common.cancel')}
          </button>
        </div>
      </form>
    </div>
  )
}

export default StoreSettingsPage

