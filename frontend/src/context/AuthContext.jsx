import React, { createContext, useContext, useEffect, useState } from 'react';
import { fetchCurrentUser } from '../services/api';

const AuthContext = createContext();

export function AuthProvider({ children }) {
  const [token, setToken] = useState(null);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [user, setUser] = useState(null);

  const loadUser = async (jwtToken) => {
    try {
      const me = await fetchCurrentUser(jwtToken);
      setUser(me);
    } catch (err) {
      console.error('Failed to load current user', err);
      setUser(null);
    }
  };

  // 🔄 Carrega token ao iniciar a aplicação
  useEffect(() => {
    const savedToken =
      localStorage.getItem('auth_token') ||
      sessionStorage.getItem('auth_token');

    if (savedToken) {
      setToken(savedToken);
      setIsAuthenticated(true);
      loadUser(savedToken);
    }
  }, []);

  const login = (jwtToken, rememberMe = false) => {
    setToken(jwtToken);
    setIsAuthenticated(true);
      loadUser(jwtToken);

    if (rememberMe) {
      localStorage.setItem('auth_token', jwtToken);
      sessionStorage.removeItem('auth_token');
    } else {
      sessionStorage.setItem('auth_token', jwtToken);
      localStorage.removeItem('auth_token');
    }
  };

  const logout = () => {
    setToken(null);
    setIsAuthenticated(false);
    setUser(null);
    localStorage.removeItem('auth_token');
    sessionStorage.removeItem('auth_token');
  };

  const isAdmin = user?.role?.name === 'admin';

  return (
    <AuthContext.Provider
      value={{
        token,
        isAuthenticated,
        user,
        isAdmin,
        login,
        logout,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  return useContext(AuthContext);
}
