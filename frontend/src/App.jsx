import { BrowserRouter, Routes, Route } from 'react-router-dom'
import { Toaster } from 'react-hot-toast'
import { useTranslation } from 'react-i18next'
import { AuthProvider } from './contexts/AuthContext'
import { TenantProvider } from './contexts/TenantContext'
import FacebookPixel from './components/FacebookPixel'

// Pages
import LoginPage from './pages/LoginPage'
import RegisterPage from './pages/RegisterPage'
import DashboardPage from './pages/DashboardPage'
import StoresPage from './pages/StoresPage'
import StoreSettingsPage from './pages/StoreSettingsPage'
import ProductsPage from './pages/ProductsPage'
import ProductFormPage from './pages/ProductFormPage'
import OrdersPage from './pages/OrdersPage'
import ShippingPage from './pages/ShippingPage'
import ProductLandingPage from './pages/ProductLandingPage'
import CheckoutPage from './pages/CheckoutPage'
import OrderConfirmationPage from './pages/OrderConfirmationPage'

// Layouts
import AppLayout from './layouts/AppLayout'
import PublicLayout from './layouts/PublicLayout'

// Protected Route
import ProtectedRoute from './components/ProtectedRoute'

function App() {
  const { i18n } = useTranslation()

  return (
    <AuthProvider>
      <TenantProvider>
        <BrowserRouter>
          <div className="min-h-screen bg-gray-50">
            <Routes>
              {/* Public routes (store pages) */}
              <Route path="/" element={<PublicLayout />}>
                <Route path="product/:slug" element={<ProductLandingPage />} />
                <Route path="checkout/:productId" element={<CheckoutPage />} />
                <Route path="order-confirmation/:orderId" element={<OrderConfirmationPage />} />
              </Route>

              {/* Auth routes */}
              <Route path="/auth" element={<PublicLayout />}>
                <Route path="login" element={<LoginPage />} />
                <Route path="register" element={<RegisterPage />} />
              </Route>

              {/* Protected app routes */}
              <Route path="/app" element={<ProtectedRoute><AppLayout /></ProtectedRoute>}>
                <Route index element={<DashboardPage />} />
                <Route path="stores" element={<StoresPage />} />
                <Route path="stores/:storeId/settings" element={<StoreSettingsPage />} />
                <Route path="stores/:storeId/products" element={<ProductsPage />} />
                <Route path="stores/:storeId/products/new" element={<ProductFormPage />} />
                <Route path="stores/:storeId/products/:productId/edit" element={<ProductFormPage />} />
                <Route path="stores/:storeId/orders" element={<OrdersPage />} />
                <Route path="stores/:storeId/shipping" element={<ShippingPage />} />
              </Route>
            </Routes>
            <Toaster position="top-center" />
          </div>
        </BrowserRouter>
        <FacebookPixel />
      </TenantProvider>
    </AuthProvider>
  )
}

export default App

