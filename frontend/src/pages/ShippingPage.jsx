import { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'
import { useTranslation } from 'react-i18next'
import api from '../utils/api'
import toast from 'react-hot-toast'

const ShippingPage = () => {
  const { t } = useTranslation()
  const { storeId } = useParams()
  const [shippingClasses, setShippingClasses] = useState([])
  const [showForm, setShowForm] = useState(false)
  const [formData, setFormData] = useState({
    name: '',
    name_bn: '',
    description: '',
    cost: '',
    is_active: true
  })
  const [loading, setLoading] = useState(true)
  const [saving, setSaving] = useState(false)

  useEffect(() => {
    loadShippingClasses()
  }, [storeId])

  const loadShippingClasses = async () => {
    try {
      const response = await api.get('/shipping')
      setShippingClasses(response.data)
      setLoading(false)
    } catch (error) {
      toast.error(t('common.error'))
      setLoading(false)
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setSaving(true)
    
    try {
      const data = {
        ...formData,
        cost: parseFloat(formData.cost)
      }
      
      await api.post('/shipping', data)
      toast.success('Shipping class created')
      setShowForm(false)
      setFormData({
        name: '',
        name_bn: '',
        description: '',
        cost: '',
        is_active: true
      })
      loadShippingClasses()
    } catch (error) {
      toast.error(error.response?.data?.detail || t('common.error'))
    } finally {
      setSaving(false)
    }
  }

  const handleDelete = async (id) => {
    if (!confirm('Are you sure?')) return
    
    try {
      await api.delete(`/shipping/${id}`)
      toast.success('Deleted')
      loadShippingClasses()
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
        <h1 className="text-3xl font-bold">{t('shipping.shippingClasses')}</h1>
        <button
          onClick={() => setShowForm(!showForm)}
          className="btn btn-primary"
        >
          {t('shipping.addShippingClass')}
        </button>
      </div>

      {showForm && (
        <div className="card mb-8">
          <h2 className="text-xl font-semibold mb-4">{t('shipping.addShippingClass')}</h2>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                {t('shipping.name')} <span className="text-red-500">*</span>
              </label>
              <input
                type="text"
                value={formData.name}
                onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                className="input"
                required
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                {t('shipping.name')} (বাংলা)
              </label>
              <input
                type="text"
                value={formData.name_bn}
                onChange={(e) => setFormData({ ...formData, name_bn: e.target.value })}
                className="input"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                {t('shipping.cost')} <span className="text-red-500">*</span>
              </label>
              <input
                type="number"
                step="0.01"
                value={formData.cost}
                onChange={(e) => setFormData({ ...formData, cost: e.target.value })}
                className="input"
                required
              />
            </div>

            <div className="flex items-center">
              <input
                type="checkbox"
                id="is_active"
                checked={formData.is_active}
                onChange={(e) => setFormData({ ...formData, is_active: e.target.checked })}
                className="mr-2"
              />
              <label htmlFor="is_active" className="text-sm font-medium text-gray-700">
                {t('shipping.active')}
              </label>
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
                onClick={() => setShowForm(false)}
                className="btn btn-secondary flex-1"
              >
                {t('common.cancel')}
              </button>
            </div>
          </form>
        </div>
      )}

      <div className="space-y-4">
        {shippingClasses.length === 0 ? (
          <div className="card text-center py-12">
            <p className="text-lg text-gray-600">No shipping classes</p>
          </div>
        ) : (
          shippingClasses.map((shipping) => (
            <div key={shipping.id} className="card">
              <div className="flex justify-between items-center">
                <div>
                  <h3 className="text-lg font-semibold">{shipping.name}</h3>
                  {shipping.name_bn && (
                    <p className="text-sm text-gray-600">{shipping.name_bn}</p>
                  )}
                  <p className="text-lg font-bold text-primary-600 mt-2">
                    ৳{shipping.cost}
                  </p>
                </div>
                <div className="flex items-center space-x-4">
                  <span className={`px-3 py-1 rounded-full text-sm ${
                    shipping.is_active
                      ? 'bg-green-100 text-green-800'
                      : 'bg-gray-100 text-gray-800'
                  }`}>
                    {shipping.is_active ? t('shipping.active') : t('shipping.inactive')}
                  </span>
                  <button
                    onClick={() => handleDelete(shipping.id)}
                    className="text-red-600 hover:text-red-700"
                  >
                    {t('common.delete')}
                  </button>
                </div>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  )
}

export default ShippingPage

