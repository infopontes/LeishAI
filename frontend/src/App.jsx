// src/App.jsx
import React from 'react';
import Header from './components/Header';
import Footer from './components/Footer';
import { useTranslation } from 'react-i18next';

function App() {
  const { t } = useTranslation();

  return (
    <div style={styles.appContainer}>
      <Header /> 
      <main style={styles.mainContent}>
        <h1>{t('greeting')}</h1>
        {/* --- Use the correct image path --- */}
        <img 
          src="/images/dsleish-hero.png" // Updated path
          alt="LeishAI main visual" 
          style={styles.heroImage} 
        />
        {/* --- END OF IMAGE --- */}
      </main>
      <Footer />
    </div>
  );
}

// Styles
const styles = {
  appContainer: { display: 'flex', flexDirection: 'column', minHeight: '100vh', },
  mainContent: { flexGrow: 1, padding: '20px', textAlign: 'center', },
  heroImage: {
    maxWidth: '80%', 
    maxHeight: '400px', 
    marginTop: '20px',
    borderRadius: '8px', 
    boxShadow: '0 4px 8px rgba(0,0,0,0.1)', 
  },
};

export default App;