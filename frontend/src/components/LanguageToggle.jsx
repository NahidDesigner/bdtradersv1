import { useTranslation } from 'react-i18next'

const LanguageToggle = () => {
  const { i18n } = useTranslation()

  const toggleLanguage = () => {
    const newLang = i18n.language === 'bn' ? 'en' : 'bn'
    i18n.changeLanguage(newLang)
  }

  return (
    <button
      onClick={toggleLanguage}
      className="px-3 py-1.5 text-sm font-medium text-gray-700 hover:text-gray-900 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors"
    >
      {i18n.language === 'bn' ? 'English' : 'বাংলা'}
    </button>
  )
}

export default LanguageToggle

