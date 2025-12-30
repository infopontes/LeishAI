import React, { useEffect, useState } from 'react';
import { useTranslation } from 'react-i18next';
import { fetchUsers, fetchRoles, updateUserAdmin } from '../services/api';
import '../styles/AdminUsers.css';

function AdminUsersPage() {
  const { t } = useTranslation();
  const [users, setUsers] = useState([]);
  const [roles, setRoles] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  const loadData = async () => {
    try {
      setLoading(true);
      setError('');
      const [u, r] = await Promise.all([fetchUsers(), fetchRoles()]);
      setUsers(u);
      setRoles(r);
    } catch (err) {
      setError(err.message || t('adminUsers.error'));
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const handleRoleChange = async (userId, roleId) => {
    try {
      setError('');
      const updated = await updateUserAdmin(userId, { role_id: roleId });
      setUsers((prev) =>
        prev.map((u) => (u.id === userId ? { ...u, role: updated.role } : u))
      );
    } catch (err) {
      setError(err.message || t('adminUsers.error'));
    }
  };

  const handleToggleActive = async (userId, isActive) => {
    try {
      setError('');
      await updateUserAdmin(userId, { is_active: isActive });
      setUsers((prev) =>
        prev.map((u) => (u.id === userId ? { ...u, is_active: isActive } : u))
      );
    } catch (err) {
      setError(err.message || t('adminUsers.error'));
    }
  };

  return (
    <div className="admin-users">
      <div className="admin-header">
        <div>
          <h2>{t('adminUsers.title')}</h2>
          <p>{t('adminUsers.description')}</p>
        </div>
        <button onClick={loadData} className="refresh-btn" disabled={loading}>
          {loading ? t('adminUsers.loading') : t('adminUsers.refresh')}
        </button>
      </div>

      {error && <p className="error-message">{error}</p>}

      {loading ? (
        <p>{t('adminUsers.loading')}</p>
      ) : (
        <div className="users-table">
          <div className="users-table__row users-table__header">
            <span>{t('adminUsers.name')}</span>
            <span>{t('adminUsers.email')}</span>
            <span>{t('adminUsers.institution')}</span>
            <span>{t('adminUsers.role')}</span>
            <span>{t('adminUsers.active')}</span>
          </div>
          {users.map((user) => (
            <div className="users-table__row" key={user.id}>
              <span>{user.full_name}</span>
              <span>{user.email}</span>
              <span>{user.institution || '-'}</span>
              <span>
                <select
                  value={user.role?.id || ''}
                  onChange={(e) => handleRoleChange(user.id, e.target.value)}
                >
                  <option value="">{t('adminUsers.noRole')}</option>
                  {roles.map((role) => (
                    <option key={role.id} value={role.id}>
                      {role.name}
                    </option>
                  ))}
                </select>
              </span>
              <span>
                <label className="toggle">
                  <input
                    type="checkbox"
                    checked={!!user.is_active}
                    onChange={(e) =>
                      handleToggleActive(user.id, e.target.checked)
                    }
                  />
                  <span>{user.is_active ? t('adminUsers.activeYes') : t('adminUsers.activeNo')}</span>
                </label>
              </span>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default AdminUsersPage;
