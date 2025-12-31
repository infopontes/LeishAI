import React from 'react';
import { useTranslation } from 'react-i18next';
import { useAuth } from '../context/AuthContext';

function ProfilePage() {
  const { t } = useTranslation();
  const { user } = useAuth();

  if (!user) {
    return <p>{t('profile.loading')}</p>;
  }

  return (
    <div className="forgot-password-container">
      <div className="forgot-password-card">
        <h2>{t('profile.title')}</h2>
        <p className="helper-text">{t('profile.description')}</p>

        <div className="profile-field">
          <strong>{t('login.emailLabel')}:</strong> <span>{user.email}</span>
        </div>
        <div className="profile-field">
          <strong>{t('register.fullName')}:</strong>{' '}
          <span>{user.full_name}</span>
        </div>
        <div className="profile-field">
          <strong>{t('register.institution')}:</strong>{' '}
          <span>{user.institution || '-'}</span>
        </div>
        <div className="profile-field">
          <strong>{t('adminUsers.role')}:</strong>{' '}
          <span>{user.role?.name || t('adminUsers.noRole')}</span>
        </div>
      </div>
    </div>
  );
}

export default ProfilePage;
