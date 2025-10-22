// src/components/Footer.jsx
import React from 'react';
import { useTranslation } from 'react-i18next';

function Footer() {
  const { t, i18n } = useTranslation(); // Get the i18n instance

  // Store the date in a standard, unambiguous format (YYYY-MM-DD)
  const updateDateISO = "2025-10-22"; 
  const version = "0.1.0"; 

  // Function to format the date based on the current language
  const formatDate = (isoDateString) => {
    try {
      const date = new Date(isoDateString + 'T00:00:00'); // Add time to avoid timezone issues
      // Map simple language codes to more specific locale codes if needed
      const localeMap = {
        en: 'en-US',
        pt: 'pt-BR',
        es: 'es-ES',
      };
      const locale = localeMap[i18n.language] || 'en-US'; // Default to US English

      // Define formatting options
      const options = { year: 'numeric', month: '2-digit', day: '2-digit' };
      
      return new Intl.DateTimeFormat(locale, options).format(date);
    } catch (error) {
      console.error("Error formatting date:", error);
      return isoDateString; // Fallback to ISO string if formatting fails
    }
  };

  const formattedUpdateDate = formatDate(updateDateISO);

  return (
    <footer style={styles.footer}>
      <p style={styles.text}>
        {t('footer.version')}: {version} | {t('footer.lastUpdatedLabel')}: {formattedUpdateDate} 
      </p>
      <p style={styles.text}>
        {t('footer.developedBy')}: {t('footer.developerTitle')} Marcelo Pontes | <a href="mailto:marcelo.rodrigues@ufpi.edu.br" style={styles.link}>marcelo.rodrigues@ufpi.edu.br</a>
      </p>
    </footer>
  );
}

// Basic inline styles (remain the same)
const styles = { /* ... styles from previous version ... */ };
styles.footer = { backgroundColor: '#343a40', color: '#f8f9fa', padding: '20px', marginTop: 'auto', textAlign: 'center', fontSize: '0.9em' };
styles.text = { margin: '5px 0' };
styles.link = { color: '#adb5bd', textDecoration: 'none' };


export default Footer;