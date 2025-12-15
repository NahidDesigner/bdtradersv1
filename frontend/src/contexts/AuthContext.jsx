import { createContext, useContext, useState, useEffect } from 'react'
import api from '../utils/api'
import toast from 'react-hot-toast'

const AuthContext = createContext()

export const useAuth = () => {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider')
  }
  return context
}

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    // Check if user is logged in
    const token = localStorage.getItem('access_token')
    const storedUser = localStorage.getItem('user')
    
    if (token && storedUser) {
      try {
        setUser(JSON.parse(storedUser))
      } catch (e) {
        localStorage.removeItem('access_token')
        localStorage.removeItem('user')
      }
    }
    setLoading(false)
  }, [])

  const login = async (phone, otp) => {
    try {
      const response = await api.post('/auth/otp/verify', { phone, otp })
      const { access_token, user } = response.data
      
      localStorage.setItem('access_token', access_token)
      localStorage.setItem('user', JSON.stringify(user))
      setUser(user)
      
      toast.success('লগইন সফল হয়েছে')
      return { success: true }
    } catch (error) {
      const message = error.response?.data?.detail || 'লগইন ব্যর্থ হয়েছে'
      toast.error(message)
      return { success: false, error: message }
    }
  }

  const requestOTP = async (phone) => {
    try {
      await api.post('/auth/otp/request', { phone })
      toast.success('ওটিপি কোড পাঠানো হয়েছে')
      return { success: true }
    } catch (error) {
      const message = error.response?.data?.detail || 'ওটিপি পাঠাতে ব্যর্থ'
      toast.error(message)
      return { success: false, error: message }
    }
  }

  const register = async (userData) => {
    try {
      const response = await api.post('/auth/register', userData)
      const { access_token, user } = response.data
      
      localStorage.setItem('access_token', access_token)
      localStorage.setItem('user', JSON.stringify(user))
      setUser(user)
      
      toast.success('অ্যাকাউন্ট তৈরি হয়েছে')
      return { success: true }
    } catch (error) {
      const message = error.response?.data?.detail || 'রেজিস্টার ব্যর্থ হয়েছে'
      toast.error(message)
      return { success: false, error: message }
    }
  }

  const logout = () => {
    localStorage.removeItem('access_token')
    localStorage.removeItem('user')
    setUser(null)
    toast.success('লগআউট হয়েছে')
  }

  return (
    <AuthContext.Provider value={{
      user,
      loading,
      login,
      requestOTP,
      register,
      logout,
      isAuthenticated: !!user
    }}>
      {children}
    </AuthContext.Provider>
  )
}

