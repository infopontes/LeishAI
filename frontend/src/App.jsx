// src/App.jsx
import React from 'react';
import Header from './components/Header';
import Footer from './components/Footer';
import { useTranslation } from 'react-i18next';
import './styles/App.css';

function App() {
  const { t } = useTranslation();

  return (
    <div className="appContainer"> 
      <Header /> 
      <main className="mainContent">
        <h1>{t('greeting')}</h1>
        <img 
          src="/images/dsleish-hero.png" 
          alt="DSLeish main visual" 
          className="heroImage" 
        />
      </main>
      <Footer />
    </div>
  );
}

export default App;