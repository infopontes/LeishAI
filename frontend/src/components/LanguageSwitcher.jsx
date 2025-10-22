// src/components/LanguageSwitcher.jsx
import React from 'react';
import { useTranslation } from 'react-i18next';
// We can import styles directly related to this component here or from Header.css
// If importing from Header.css, no separate import needed if Header imports it.
// Let's assume styles are in Header.css for simplicity for now.

const flags = {
  en: '/images/us.svg', pt: '/images/br.svg', es: '/images/es.svg',
};
const languages = [
  { code: 'en', name: 'English', flag: flags.en },
  { code: 'pt', name: 'Português', flag: flags.pt },
  { code: 'es', name: 'Español', flag: flags.es },
];

function LanguageSwitcher() {
  const { i18n } = useTranslation();
  const changeLanguage = (lng) => { i18n.changeLanguage(lng); };

  return (
    <div className="languageSwitcherContainer"> {/* Use className */}
      {languages.map((lang) => (
        <button
          key={lang.code}
          className="languageButton" // Use className
          onClick={() => changeLanguage(lang.code)}
          disabled={i18n.resolvedLanguage === lang.code} 
          title={lang.name}
        >
          <img src={lang.flag} alt={`${lang.name} flag`} className="flagImage" /> {/* Use className */}
        </button>
      ))}
    </div>
  );
}
// Remove the inline styles object 'styles'
export default LanguageSwitcher;