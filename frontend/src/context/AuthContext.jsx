import React, { createContext, useContext, useEffect, useState } from 'react';

const AuthContext = createContext();

export function AuthProvider({ children }) {
  const [token, setToken] = useState(null);
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  // 🔄 Carrega token ao iniciar a aplicação
  useEffect(() => {
    const savedToken =
      localStorage.getItem('auth_token') ||
      sessionStorage.getItem('auth_token');

    if (savedToken) {
      setToken(savedToken);
      setIsAuthenticated(true);
    }
  }, []);

  const login = (jwtToken, rememberMe = false) => {
    setToken(jwtToken);
    setIsAuthenticated(true);

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
    localStorage.removeItem('auth_token');
    sessionStorage.removeItem('auth_token');
  };

  return (
    <AuthContext.Provider
      value={{
        token,
        isAuthenticated,
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
