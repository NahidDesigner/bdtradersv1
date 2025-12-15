import { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { useTranslation } from 'react-i18next'
import { useAuth } from '../contexts/AuthContext'

const LoginPage = () => {
  const { t } = useTranslation()
  const { login, requestOTP } = useAuth()
  const navigate = useNavigate()
  
  const [phone, setPhone] = useState('')
  const [otp, setOtp] = useState('')
  const [step, setStep] = useState('phone') // 'phone' or 'otp'
  const [loading, setLoading] = useState(false)

  const handleRequestOTP = async (e) => {
    e.preventDefault()
    if (!phone) {
      return
    }
    
    setLoading(true)
    const result = await requestOTP(phone)
    setLoading(false)
    
    if (result.success) {
      setStep('otp')
    }
  }

  const handleVerifyOTP = async (e) => {
    e.preventDefault()
    if (!otp) {
      return
    }
    
    setLoading(true)
    const result = await login(phone, otp)
    setLoading(false)
    
    if (result.success) {
      navigate('/app')
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center px-4 py-12">
      <div className="max-w-md w-full">
        <div className="card">
          <h1 className="text-2xl font-bold text-center mb-6">
            {t('auth.login')}
          </h1>

          {step === 'phone' ? (
            <form onSubmit={handleRequestOTP} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  {t('auth.phone')}
                </label>
                <input
                  type="tel"
                  value={phone}
                  onChange={(e) => setPhone(e.target.value)}
                  placeholder={t('auth.enterPhone')}
                  className="input"
                  required
                />
              </div>
              
              <button
                type="submit"
                disabled={loading}
                className="btn btn-primary w-full touch-target"
              >
                {loading ? t('common.loading') : t('auth.sendCode')}
              </button>
            </form>
          ) : (
            <form onSubmit={handleVerifyOTP} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  {t('auth.otp')}
                </label>
                <input
                  type="text"
                  value={otp}
                  onChange={(e) => setOtp(e.target.value.replace(/\D/g, '').slice(0, 6))}
                  placeholder={t('auth.enterOTP')}
                  className="input text-center text-2xl tracking-widest"
                  maxLength={6}
                  required
                />
                <p className="text-sm text-gray-500 mt-2">
                  {t('auth.otpSent')}: {phone}
                </p>
              </div>
              
              <button
                type="submit"
                disabled={loading}
                className="btn btn-primary w-full touch-target"
              >
                {loading ? t('common.loading') : t('auth.verifyCode')}
              </button>
              
              <button
                type="button"
                onClick={() => setStep('phone')}
                className="text-sm text-primary-600 hover:text-primary-700 w-full"
              >
                {t('common.back')}
              </button>
            </form>
          )}

          <div className="mt-6 text-center">
            <p className="text-sm text-gray-600">
              {t('auth.alreadyHaveAccount')}{' '}
              <Link to="/auth/register" className="text-primary-600 hover:text-primary-700 font-medium">
                {t('auth.register')}
              </Link>
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}

export default LoginPage

