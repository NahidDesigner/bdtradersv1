import { createContext, useContext, useState, useEffect } from 'react'
import api from '../utils/api'

const TenantContext = createContext()

export const useTenant = () => {
  const context = useContext(TenantContext)
  if (!context) {
    throw new Error('useTenant must be used within TenantProvider')
  }
  return context
}

export const TenantProvider = ({ children }) => {
  const [currentTenant, setCurrentTenant] = useState(null)
  const [tenants, setTenants] = useState([])

  // Extract tenant from subdomain
  useEffect(() => {
    const hostname = window.location.hostname
    const parts = hostname.split('.')
    
    // If subdomain exists and is not www/api/app
    if (parts.length >= 3) {
      const subdomain = parts[0]
      if (!['www', 'api', 'app', 'admin'].includes(subdomain)) {
        // Load tenant by slug
        loadTenantBySlug(subdomain)
      }
    }
  }, [])

  const loadTenantBySlug = async (slug) => {
    try {
      const response = await api.get(`/tenants/slug/${slug}`)
      setCurrentTenant(response.data)
    } catch (error) {
      console.error('Failed to load tenant:', error)
    }
  }

  const loadUserTenants = async () => {
    try {
      const response = await api.get('/tenants')
      setTenants(response.data)
    } catch (error) {
      console.error('Failed to load tenants:', error)
    }
  }

  const createTenant = async (tenantData) => {
    try {
      const response = await api.post('/tenants', tenantData)
      await loadUserTenants()
      return { success: true, data: response.data }
    } catch (error) {
      return { 
        success: false, 
        error: error.response?.data?.detail || 'Failed to create store' 
      }
    }
  }

  const updateTenant = async (tenantId, tenantData) => {
    try {
      const response = await api.put(`/tenants/${tenantId}`, tenantData)
      await loadUserTenants()
      if (currentTenant?.id === tenantId) {
        setCurrentTenant(response.data)
      }
      return { success: true, data: response.data }
    } catch (error) {
      return { 
        success: false, 
        error: error.response?.data?.detail || 'Failed to update store' 
      }
    }
  }

  return (
    <TenantContext.Provider value={{
      currentTenant,
      tenants,
      loadUserTenants,
      createTenant,
      updateTenant,
      setCurrentTenant
    }}>
      {children}
    </TenantContext.Provider>
  )
}

