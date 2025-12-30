import { Link } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { useAuth } from '../context/AuthContext';
import Logout from './Logout';
import LanguageSwitcher from './LanguageSwitcher';
import '../styles/Header.css';

function Header() {
  const { t } = useTranslation();
  const { isAuthenticated } = useAuth();

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

          {isAuthenticated && (
            <>
              <Link to="/admin/users" className="navLink">
                {t('menu.admin')}
              </Link>
              <Logout />
            </>
          )}
        </div>

        <LanguageSwitcher />
      </nav>
    </header>
  );
}

export default Header;
