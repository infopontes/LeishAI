import React from 'react';
import { useTranslation } from 'react-i18next';
import { useAuth } from '../context/AuthContext';

import '../styles/Profile.css';

function ProfilePage() {
  const { t } = useTranslation();
  const { user } = useAuth();

  if (!user) {
    return <p className="profile-loading">{t('profile.loading')}</p>;
  }

  return (
    <div className="profile-page">
      <div className="profile-card">
        <div className="profile-header">
          <div className="avatar-circle">
            {user.full_name ? user.full_name[0]?.toUpperCase() : '?'}
          </div>
          <div>
            <h2>{user.full_name || t('profile.title')}</h2>
            <p className="email-text">{user.email}</p>
          </div>
        </div>

        <div className="profile-grid">
          <div>
            <p className="label">{t('login.emailLabel')}</p>
            <p className="value">{user.email}</p>
          </div>
          <div>
            <p className="label">{t('register.fullName')}</p>
            <p className="value">{user.full_name}</p>
          </div>
          <div>
            <p className="label">{t('register.institution')}</p>
            <p className="value">{user.institution || '-'}</p>
          </div>
          <div>
            <p className="label">{t('adminUsers.role')}</p>
            <p className="value">
              {t(`adminUsers.roleLabels.${user.role?.name}`, {
                defaultValue: user.role?.name || t('adminUsers.noRole'),
              })}
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}

export default ProfilePage;
