import { useFetch } from '../hooks/useFetch'
import { getMe } from '../api/users'
import { useAuth } from '../context/AuthContext'
import Spinner from '../components/Spinner'
import { PageTitle, Card, SectionTitle } from '../components/ui'

const ROLE_LABELS = {
  user: 'Сотрудник',
  moderator: 'Модератор',
  admin: 'Администратор',
  super_admin: 'Суперадминистратор',
}

const WORK_MODE_LABELS = {
  daily: 'Ежедневный (8 ч/отгул)',
  shift: 'Сменный (24 ч/отгул)',
}

function InfoRow({ label, value }) {
  return (
    <div
      style={{
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        padding: '11px 0',
        borderBottom: '1px solid rgba(30,58,90,0.5)',
      }}
    >
      <span style={{ color: '#64748b', fontSize: 12, fontWeight: 500, textTransform: 'uppercase', letterSpacing: '0.4px' }}>
        {label}
      </span>
      <span style={{ color: '#e2e8f0', fontSize: 13, fontWeight: 500 }}>
        {value || '—'}
      </span>
    </div>
  )
}

export default function Profile() {
  const { tokenData } = useAuth()
  const { data: user, loading, error } = useFetch(getMe)

  if (loading) return <Spinner />

  const fullName = user
    ? [user.surname, user.first_name, user.patronymic].filter(Boolean).join(' ')
    : null

  const initials = fullName
    ? fullName.split(' ').map(w => w[0]).slice(0, 2).join('')
    : '?'

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 20 }}>
      <PageTitle>Профиль</PageTitle>

      {error && (
        <div style={{ color: '#f87171', fontSize: 13, padding: '10px 0' }}>{error}</div>
      )}

      {user && (
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: 16 }}>
          {/* Avatar card */}
          <Card style={{ padding: 24 }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: 16, marginBottom: 20, paddingBottom: 20, borderBottom: '1px solid #1e3a5a' }}>
              <div
                style={{
                  width: 64,
                  height: 64,
                  background: 'linear-gradient(135deg, #c81e1e, #a61818)',
                  borderRadius: 14,
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  fontWeight: 700,
                  fontSize: 22,
                  color: 'white',
                  flexShrink: 0,
                  boxShadow: '0 4px 16px rgba(200,30,30,0.3)',
                }}
              >
                {initials}
              </div>
              <div>
                <div style={{ color: '#f1f5f9', fontWeight: 700, fontSize: 16 }}>
                  {fullName || '—'}
                </div>
                <div style={{ color: '#c81e1e', fontSize: 11, fontWeight: 600, textTransform: 'uppercase', letterSpacing: '0.5px', marginTop: 2 }}>
                  {ROLE_LABELS[user.role] || user.role}
                </div>
                <div style={{ color: '#64748b', fontSize: 11, marginTop: 2 }}>
                  @{user.login}
                </div>
              </div>
            </div>

            <InfoRow label="Логин" value={user.login} />
            <InfoRow label="Роль" value={ROLE_LABELS[user.role] || user.role} />
            <InfoRow label="Режим работы" value={WORK_MODE_LABELS[user.work_mode] || user.work_mode} />
            <InfoRow
              label="Статус"
              value={
                <span style={{ color: user.is_active ? '#4ade80' : '#f87171' }}>
                  {user.is_active ? '● Активен' : '○ Неактивен'}
                </span>
              }
            />
          </Card>

          {/* Details card */}
          <Card style={{ padding: 24 }}>
            <SectionTitle style={{ marginBottom: 16 }}>Служебная информация</SectionTitle>
            <InfoRow label="Звание" value={user.rank} />
            <InfoRow label="Должность" value={user.position} />
            <InfoRow label="Подразделение (ID)" value={user.department_id} />
            <InfoRow label="Организация (ID)" value={user.organization_id} />
            <InfoRow label="Дата регистрации" value={user.created_at?.slice(0, 10)} />
          </Card>
        </div>
      )}

      {/* Token info */}
      {tokenData && (
        <Card style={{ padding: 16 }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: 10, flexWrap: 'wrap' }}>
            <span style={{ color: '#64748b', fontSize: 11, textTransform: 'uppercase', letterSpacing: '0.5px' }}>
              JWT токен:
            </span>
            <span style={{ color: '#93c5fd', fontSize: 11 }}>
              Роль: <strong>{tokenData.role}</strong>
            </span>
            <span style={{ color: '#64748b', fontSize: 11 }}>•</span>
            <span style={{ color: '#93c5fd', fontSize: 11 }}>
              Отдел ID: <strong>{tokenData.department_id}</strong>
            </span>
            <span style={{ color: '#64748b', fontSize: 11 }}>•</span>
            <span style={{ color: '#93c5fd', fontSize: 11 }}>
              Орг ID: <strong>{tokenData.organization_id}</strong>
            </span>
          </div>
        </Card>
      )}
    </div>
  )
}
