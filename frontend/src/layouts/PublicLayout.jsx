import { Outlet } from 'react-router-dom'
import LanguageToggle from '../components/LanguageToggle'

const PublicLayout = () => {
  return (
    <div className="min-h-screen bg-gray-50">
      {/* Simple header for public pages */}
      <header className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-end items-center h-14">
            <LanguageToggle />
          </div>
        </div>
      </header>

      <Outlet />
    </div>
  )
}

export default PublicLayout

