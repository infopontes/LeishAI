import { Link, useNavigate } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { useAuth } from '../context/AuthContext';
import LanguageSwitcher from './LanguageSwitcher';
import '../styles/Header.css';
import { useState } from 'react';

function Header() {
  const { t } = useTranslation();
  const navigate = useNavigate();
  const { isAuthenticated, isAdmin, user, logout } = useAuth();
  const [menuOpen, setMenuOpen] = useState(false);

  const roleLabel = user?.role?.name
    ? t(`adminUsers.roleLabels.${user.role.name}`, { defaultValue: user.role.name })
    : t('adminUsers.noRole');

  return (
    <header className="header">
      <nav className="nav">
        <div className="navLinks">
          <Link to="/" className="navLink">{t('menu.home')}</Link>
          <Link to="/about" className="navLink">{t('menu.about')}</Link>

          {!isAuthenticated && (
            <Link to="/login" className="navLink">
              {t('menu.login')}
            </Link>
          )}
        </div>

        <div className="navRight">
          <LanguageSwitcher />
          {isAuthenticated && (
            <>
              {isAdmin && (
                <Link to="/admin/users" className="navLink">
                  {t('menu.admin')}
                </Link>
              )}
              <div className="userMenu">
                <button
                  className="userMenu__button"
                  onClick={() => setMenuOpen((prev) => !prev)}
                >
                  <span className="userMenu__name">
                    {user?.full_name || t('menu.profile')}
                  </span>
                  <span className="userMenu__role">{roleLabel}</span>
                </button>
                {menuOpen && (
                  <div className="userMenu__dropdown">
                    <Link
                      to="/profile"
                      className="dropdown-link"
                      onClick={() => setMenuOpen(false)}
                    >
                      {t('menu.profile')}
                    </Link>
                    <button
                      className="dropdown-link"
                      onClick={() => {
                        setMenuOpen(false);
                        logout();
                        navigate('/login');
                      }}
                    >
                      {t('menu.logout')}
                    </button>
                  </div>
                )}
              </div>
            </>
          )}
        </div>
      </nav>
    </header>
  );
}

export default Header;
