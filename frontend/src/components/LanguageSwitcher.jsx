// src/components/LanguageSwitcher.jsx
import React from 'react';
import { useTranslation } from 'react-i18next';

// Use the actual image paths relative to the public folder
const flags = {
  en: '/images/us.svg', // Path to US flag
  pt: '/images/br.svg', // Path to Brazil flag
  es: '/images/es.svg', // Path to Spain flag
};

const languages = [
  { code: 'en', name: 'English', flag: flags.en },
  { code: 'pt', name: 'Português', flag: flags.pt },
  { code: 'es', name: 'Español', flag: flags.es },
];

function LanguageSwitcher() {
  const { i18n } = useTranslation();

  const changeLanguage = (lng) => {
    i18n.changeLanguage(lng);
  };

  return (
    <div style={styles.container}>
      {languages.map((lang) => (
        <button
          key={lang.code}
          style={{
            ...styles.button,
            // Add slight dimming effect if disabled
            opacity: i18n.resolvedLanguage === lang.code ? 0.5 : 1, 
            cursor: i18n.resolvedLanguage === lang.code ? 'default' : 'pointer',
          }}
          onClick={() => changeLanguage(lang.code)}
          disabled={i18n.resolvedLanguage === lang.code} 
          title={lang.name}
        >
          {/* Use img tag for the flag */}
          <img src={lang.flag} alt={`${lang.name} flag`} style={styles.flag} />
        </button>
      ))}
    </div>
  );
}

// Updated styles
const styles = {
  container: {
    display: 'flex',
    gap: '10px',
    alignItems: 'center', // Align flags vertically
  },
  button: {
    background: 'none',
    border: 'none',
    padding: '0',
    lineHeight: 0, // Prevent extra space around image
  },
  flag: {
    width: '24px', // Set a specific size for the flags
    height: 'auto',
    display: 'block', // Ensure image behaves like a block element
  }
};

export default LanguageSwitcher;