// src/components/Header.jsx
import React from 'react';
import { useTranslation } from 'react-i18next'; // Hook para buscar traduções
import LanguageSwitcher from './LanguageSwitcher';

function Header() {
  const { t } = useTranslation(); // Inicializa o hook de tradução

  return (
    <header style={styles.header}>
      <nav style={styles.nav}>
        {/* Placeholder for Logo if needed */}
        {/* <img src="/path/to/logo.png" alt="LeishAI Logo" style={styles.logo} /> */}
        
        <div style={styles.navLinks}>
          <a href="/" style={styles.navLink}>{t('menu.home')}</a>
          <a href="/about" style={styles.navLink}>{t('menu.about')}</a>
          {/* Placeholder for Login/Logout Link */}
          <a href="/login" style={styles.navLink}>{t('menu.login')}</a>
        </div>
        
        <LanguageSwitcher />
      </nav>
    </header>
  );
}

// Basic inline styles (we'll improve this later with CSS files)
const styles = {
  header: {
    backgroundColor: '#f8f9fa', // Light gray background
    padding: '10px 20px',
    borderBottom: '1px solid #dee2e6', // Subtle border
  },
  nav: {
    display: 'flex',
    justifyContent: 'space-between', // Pushes items apart
    alignItems: 'center',
  },
  navLinks: {
    display: 'flex',
    gap: '20px', // Space between links
  },
  navLink: {
    textDecoration: 'none',
    color: '#007bff', // Blue link color
    fontWeight: 'bold',
  },
  languageSwitcher: {
    // Styles for the language switcher area
  },
  // logo: { height: '40px' } // Example style for a logo
};

export default Header;