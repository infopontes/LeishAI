import React, { useEffect, useState } from 'react';
import { useTranslation } from 'react-i18next';
import {
  fetchUsers,
  fetchRoles,
  updateUserAdmin,
  registerUser,
} from '../services/api';
import '../styles/AdminUsers.css';

function AdminUsersPage() {
  const { t } = useTranslation();
  const [users, setUsers] = useState([]);
  const [roles, setRoles] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [sortConfig, setSortConfig] = useState({ key: 'full_name', dir: 'asc' });
  const [showCreate, setShowCreate] = useState(false);
  const [createData, setCreateData] = useState({
    fullName: '',
    email: '',
    institution: '',
    password: '',
    roleId: '',
  });

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

  const sortUsers = (key) => {
    setSortConfig((prev) => {
      const dir = prev.key === key && prev.dir === 'asc' ? 'desc' : 'asc';
      const sorted = [...users].sort((a, b) => {
        const aVal = (a[key] || '').toString().toLowerCase();
        const bVal = (b[key] || '').toString().toLowerCase();
        if (aVal < bVal) return dir === 'asc' ? -1 : 1;
        if (aVal > bVal) return dir === 'asc' ? 1 : -1;
        return 0;
      });
      setUsers(sorted);
      return { key, dir };
    });
  };

  const SortIcon = ({ column }) => {
    if (sortConfig.key !== column) return <span className="sort-icon">↕</span>;
    return sortConfig.dir === 'asc' ? (
      <span className="sort-icon">↑</span>
    ) : (
      <span className="sort-icon">↓</span>
    );
  };

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

  const translateRoleName = (roleName) =>
    t(`adminUsers.roleLabels.${roleName}`, { defaultValue: roleName });

  return (
    <div className="admin-users">
      <div className="admin-header">
        <div>
          <h2>{t('adminUsers.title')}</h2>
          <p>{t('adminUsers.description')}</p>
        </div>
        <div className="admin-actions">
          <button onClick={loadData} className="refresh-btn" disabled={loading}>
            {loading ? t('adminUsers.loading') : t('adminUsers.refresh')}
          </button>
          <button
            className="refresh-btn ghost"
            onClick={() => setShowCreate((p) => !p)}
          >
            {showCreate ? t('adminUsers.hideCreate') : t('adminUsers.showCreate')}
          </button>
        </div>
      </div>

      {error && <p className="error-message">{error}</p>}

      {showCreate && (
        <div className="create-user-card">
          <h3>{t('adminUsers.createTitle')}</h3>
          <div className="create-grid">
            <label>
              {t('register.fullName')}
              <input
                value={createData.fullName}
                onChange={(e) =>
                  setCreateData((prev) => ({ ...prev, fullName: e.target.value }))
                }
              />
            </label>
            <label>
              {t('login.emailLabel')}
              <input
                type="email"
                value={createData.email}
                onChange={(e) =>
                  setCreateData((prev) => ({ ...prev, email: e.target.value }))
                }
              />
            </label>
            <label>
              {t('register.institution')}
              <input
                value={createData.institution}
                onChange={(e) =>
                  setCreateData((prev) => ({
                    ...prev,
                    institution: e.target.value,
                  }))
                }
              />
            </label>
            <label>
              {t('login.passwordLabel')}
              <input
                type="password"
                value={createData.password}
                onChange={(e) =>
                  setCreateData((prev) => ({ ...prev, password: e.target.value }))
                }
              />
            </label>
            <label>
              {t('adminUsers.role')}
              <select
                value={createData.roleId}
                onChange={(e) =>
                  setCreateData((prev) => ({ ...prev, roleId: e.target.value }))
                }
              >
                <option value="">{t('adminUsers.noRole')}</option>
                {roles.map((role) => (
                  <option key={role.id} value={role.id}>
                    {translateRoleName(role.name)}
                  </option>
                ))}
              </select>
            </label>
          </div>
          <button
            className="refresh-btn"
            onClick={async () => {
              setError('');
              if (!createData.fullName || !createData.email || !createData.password) {
                setError(t('register.error.missingFields'));
                return;
              }
              if (createData.password.length < 8) {
                setError(t('register.error.tooShort'));
                return;
              }
              try {
                const newUser = await registerUser({
                  fullName: createData.fullName,
                  email: createData.email,
                  institution: createData.institution,
                  password: createData.password,
                  reason: 'Created by admin panel',
                });
                if (createData.roleId) {
                  const updated = await updateUserAdmin(newUser.id, {
                    role_id: createData.roleId,
                    is_active: true,
                  });
                  setUsers((prev) => [...prev, updated]);
                } else {
                  setUsers((prev) => [
                    ...prev,
                    { ...newUser, is_active: true, role: null },
                  ]);
                }
                setCreateData({
                  fullName: '',
                  email: '',
                  institution: '',
                  password: '',
                  roleId: '',
                });
                setShowCreate(false);
              } catch (err) {
                setError(err.message || t('adminUsers.error'));
              }
            }}
          >
            {t('adminUsers.createButton')}
          </button>
        </div>
      )}

      {loading ? (
        <p>{t('adminUsers.loading')}</p>
      ) : (
        <div className="users-table">
          <div className="users-table__row users-table__header">
            <button
              type="button"
              className="header-sort"
              onClick={() => sortUsers('full_name')}
            >
              {t('adminUsers.name')} <SortIcon column="full_name" />
            </button>
            <button
              type="button"
              className="header-sort"
              onClick={() => sortUsers('email')}
            >
              {t('adminUsers.email')} <SortIcon column="email" />
            </button>
            <button
              type="button"
              className="header-sort"
              onClick={() => sortUsers('institution')}
            >
              {t('adminUsers.institution')} <SortIcon column="institution" />
            </button>
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
                      {translateRoleName(role.name)}
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
