// src/components/Footer.jsx
import React from 'react';
import { useTranslation } from 'react-i18next';
import '../styles/Footer.css';

function Footer() {
  const { t, i18n } = useTranslation();
  const updateDateISO = "2025-10-22"; 
  const version = "0.1.0"; 

  const formatDate = (isoDateString) => {
    try {
      const date = new Date(isoDateString + 'T00:00:00'); 
      const localeMap = { en: 'en-US', pt: 'pt-BR', es: 'es-ES' };
      const locale = localeMap[i18n.language] || 'en-US'; 
      const options = { year: 'numeric', month: '2-digit', day: '2-digit' };
      return new Intl.DateTimeFormat(locale, options).format(date);
    } catch (error) {
      console.error("Error formatting date:", error);
      return isoDateString; 
    }
  };
  const formattedUpdateDate = formatDate(updateDateISO);

  return (
    // Use className instead of style
    <footer className="footer">
      <p className="footerText">
        {t('footer.version')}: {version} | {t('footer.lastUpdatedLabel')}: {formattedUpdateDate} 
      </p>
      <p className="footerText">
        {t('footer.developedBy')}: {t('footer.developerTitle')} Marcelo Pontes | <a href="mailto:marcelo.rodrigues@ufpi.edu.br" className="footerLink">marcelo.rodrigues@ufpi.edu.br</a>
      </p>
    </footer>
  );
}
// Remove the inline styles object 'styles'
export default Footer;