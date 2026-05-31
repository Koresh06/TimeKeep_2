import { useFetch } from '../hooks/useFetch'
import { getMyOvertimes } from '../api/overtimes'
import { getMyDayOffs } from '../api/dayoffs'
import { useAuth } from '../context/AuthContext'
import Spinner from '../components/Spinner'
import {
  PageTitle, StatCard, Card, SectionTitle,
  StatusBadge, TableContainer, Table, THead, Th, Td, TRow, EmptyState,
} from '../components/ui'
import { Link } from 'react-router-dom'

const ROLE_LABELS = {
  user: 'Сотрудник',
  moderator: 'Модератор',
  admin: 'Администратор',
  super_admin: 'Суперадминистратор',
}

const WORK_MODE_LABELS = {
  daily: 'Ежедневный режим',
  shift: 'Сменный режим',
}

function totalDurationH(overtimes = []) {
  return overtimes.reduce((acc, o) => {
    const [fh, fm] = (o.start_time || '0:0').split(':').map(Number)
    const [th, tm] = (o.end_time || '0:0').split(':').map(Number)
    return acc + (th * 60 + tm - (fh * 60 + fm)) / 60
  }, 0)
}

function availableHours(overtimes = []) {
  return overtimes
    .filter(o => o.status === 'active')
    .reduce((acc, o) => {
      const [fh, fm] = (o.start_time || '0:0').split(':').map(Number)
      const [th, tm] = (o.end_time || '0:0').split(':').map(Number)
      const dur = (th * 60 + tm - (fh * 60 + fm)) / 60
      return acc + Math.max(dur - (o.used_hours || 0), 0)
    }, 0)
}

function formatH(h) {
  const hours = Math.floor(h)
  const mins = Math.round((h - hours) * 60)
  return mins > 0 ? `${hours} ч ${mins} мин` : `${hours} ч`
}

export default function Dashboard() {
  const { tokenData } = useAuth()
  const { data: overtimes, loading: lo } = useFetch(getMyOvertimes)
  const { data: dayoffs, loading: ld } = useFetch(getMyDayOffs)

  if (lo || ld) return <Spinner />

  const total = totalDurationH(overtimes)
  const avail = availableHours(overtimes)
  const recent = (dayoffs || []).slice(-5).reverse()

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 24 }}>
      {/* Header */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', flexWrap: 'wrap', gap: 8 }}>
        <div>
          <PageTitle>Главная панель</PageTitle>
          <p style={{ color: '#64748b', fontSize: 12, margin: '4px 0 0' }}>
            {ROLE_LABELS[tokenData?.role] || 'Сотрудник'} ·{' '}
            {WORK_MODE_LABELS[tokenData?.work_mode] || ''}
          </p>
        </div>
        <div
          style={{
            background: 'rgba(200,30,30,0.08)',
            border: '1px solid rgba(200,30,30,0.2)',
            borderRadius: 8,
            padding: '6px 14px',
            display: 'flex',
            alignItems: 'center',
            gap: 8,
          }}
        >
          <div style={{ width: 8, height: 8, background: '#22c55e', borderRadius: '50%' }} />
          <span style={{ color: '#94a3b8', fontSize: 12 }}>Система активна</span>
        </div>
      </div>

      {/* Stats grid */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(180px, 1fr))', gap: 14 }}>
        <StatCard
          label="Переработок"
          value={(overtimes || []).length}
          sub="Всего записей"
          color="#c81e1e"
        />
        <StatCard
          label="Всего часов"
          value={formatH(total)}
          sub="Накоплено"
          color="#1a4b8c"
        />
        <StatCard
          label="Доступно"
          value={formatH(avail)}
          sub="Для отгула"
          color="#16a34a"
        />
        <StatCard
          label="Отгулов"
          value={(dayoffs || []).length}
          sub="Всего заявок"
          color="#d97706"
        />
      </div>

      {/* Recent day-offs + quick access */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: 16 }}>
        {/* Recent day-offs */}
        <Card>
          <div style={{ padding: '16px 16px 12px', display: 'flex', justifyContent: 'space-between', alignItems: 'center', borderBottom: '1px solid #1e3a5a' }}>
            <SectionTitle>Последние отгулы</SectionTitle>
            <Link to="/day-offs" style={{ color: '#93c5fd', fontSize: 11, textDecoration: 'none', fontWeight: 500 }}>
              Все →
            </Link>
          </div>
          {recent.length === 0 ? (
            <EmptyState message="Нет заявок на отгул" />
          ) : (
            <div>
              {recent.map((d) => (
                <div
                  key={d.id}
                  style={{
                    padding: '10px 16px',
                    display: 'flex',
                    justifyContent: 'space-between',
                    alignItems: 'center',
                    borderBottom: '1px solid rgba(30,58,90,0.4)',
                  }}
                >
                  <div>
                    <span style={{ color: '#e2e8f0', fontSize: 13, fontWeight: 500 }}>
                      {d.date_}
                    </span>
                    <div style={{ color: '#64748b', fontSize: 11, marginTop: 1 }}>
                      {d.overtimes?.length || 0} переработок
                    </div>
                  </div>
                  <StatusBadge status={d.status} />
                </div>
              ))}
            </div>
          )}
        </Card>

        {/* Recent overtimes */}
        <Card>
          <div style={{ padding: '16px 16px 12px', display: 'flex', justifyContent: 'space-between', alignItems: 'center', borderBottom: '1px solid #1e3a5a' }}>
            <SectionTitle>Последние переработки</SectionTitle>
            <Link to="/overtimes" style={{ color: '#93c5fd', fontSize: 11, textDecoration: 'none', fontWeight: 500 }}>
              Все →
            </Link>
          </div>
          {(!overtimes || overtimes.length === 0) ? (
            <EmptyState message="Нет записей переработок" />
          ) : (
            <div>
              {[...(overtimes || [])].reverse().slice(0, 5).map((o) => (
                <div
                  key={o.id}
                  style={{
                    padding: '10px 16px',
                    display: 'flex',
                    justifyContent: 'space-between',
                    alignItems: 'center',
                    borderBottom: '1px solid rgba(30,58,90,0.4)',
                  }}
                >
                  <div>
                    <span style={{ color: '#e2e8f0', fontSize: 13, fontWeight: 500 }}>
                      {o.date_}
                    </span>
                    <div style={{ color: '#64748b', fontSize: 11, marginTop: 1 }}>
                      {o.start_time?.slice(0, 5)} — {o.end_time?.slice(0, 5)}
                    </div>
                  </div>
                  <StatusBadge status={o.status} />
                </div>
              ))}
            </div>
          )}
        </Card>
      </div>

      {/* Quick action links */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: 12 }}>
        {[
          { to: '/overtimes', label: '+ Добавить переработку', color: '#1a4b8c' },
          { to: '/day-offs', label: '+ Оформить отгул', color: '#c81e1e' },
          { to: '/statistics', label: '📊 Моя статистика', color: '#16a34a' },
        ].map(({ to, label, color }) => (
          <Link
            key={to}
            to={to}
            style={{
              background: `rgba(${color === '#c81e1e' ? '200,30,30' : color === '#1a4b8c' ? '26,75,140' : '22,163,74'},0.1)`,
              border: `1px solid ${color}33`,
              borderRadius: 8,
              padding: '12px 16px',
              color,
              fontSize: 13,
              fontWeight: 600,
              textDecoration: 'none',
              display: 'block',
              textAlign: 'center',
              transition: 'background 0.15s',
            }}
          >
            {label}
          </Link>
        ))}
      </div>
    </div>
  )
}
