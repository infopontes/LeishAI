// src/App.jsx
import React from 'react';
import { Routes, Route, Outlet } from 'react-router-dom';
import Header from './components/Header';
import Footer from './components/Footer';
import HomePage from './pages/HomePage';
import AboutPage from './pages/AboutPage';
import LoginPage from './pages/LoginPage';
import ForgotPasswordPage from './pages/ForgotPasswordPage';
import PredictionPage from './pages/PredictionPage';
import './styles/App.css'; 

function Layout() {
  return (
    <div className="appContainer">
      <Header />
      <main className="mainContent">
        <Outlet />
      </main>
      <Footer />
    </div>
  );
}

function App() {
  return (
    <Routes>
      <Route path="/" element={<Layout />}>
        <Route index element={<HomePage />} />
        <Route path="about" element={<AboutPage />} />
        <Route path="login" element={<LoginPage />} />
        <Route path="forgot-password" element={<ForgotPasswordPage />} />
        <Route path="predict" element={<PredictionPage />} />
      </Route>
    </Routes>
  );
}

export default App;
