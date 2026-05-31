import { useState, useEffect } from 'react'
import { useAuth, hasRole } from '../context/AuthContext'
import {
  getMyStatistics,
  getDepartmentStatistics,
  getOrganizationStatistics,
  getAllStatistics,
} from '../api/statistics'
import Spinner from '../components/Spinner'
import { PageTitle, StatCard, Card, SectionTitle } from '../components/ui'

const MONTHS_RU = ['Янв','Фев','Мар','Апр','Май','Июн','Июл','Авг','Сен','Окт','Ноя','Дек']

function BarChart({ data, height = 140 }) {
  if (!data || !data.length) {
    return (
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', height: height + 40, color: '#1e3a5a', fontSize: 13 }}>
        Нет данных
      </div>
    )
  }

  const max = Math.max(...data.map(d => d.value), 0.1)
  const barW = 32
  const gap = 14
  const padL = 8
  const padB = 28
  const svgW = padL + data.length * (barW + gap) - gap + padL
  const svgH = height + padB

  return (
    <div style={{ overflowX: 'auto' }}>
      <svg width={svgW} height={svgH} style={{ display: 'block' }}>
        {/* Grid lines */}
        {[0.25, 0.5, 0.75, 1].map(ratio => (
          <line
            key={ratio}
            x1={0}
            y1={height - height * ratio}
            x2={svgW}
            y2={height - height * ratio}
            stroke="#1e3a5a"
            strokeWidth={1}
            strokeDasharray="4 4"
          />
        ))}

        {data.map((d, i) => {
          const barH = max > 0 ? Math.round((d.value / max) * height) : 2
          const x = padL + i * (barW + gap)
          const y = height - barH
          return (
            <g key={i}>
              {/* Bar shadow */}
              <rect x={x + 2} y={y + 2} width={barW} height={barH} fill="rgba(200,30,30,0.08)" rx={4} />
              {/* Bar */}
              <rect
                x={x} y={y} width={barW} height={barH}
                fill="url(#barGrad)" rx={4}
              />
              {/* Value label */}
              {d.value > 0 && (
                <text
                  x={x + barW / 2} y={y - 5}
                  textAnchor="middle" fontSize={10} fill="#e2e8f0" fontWeight="600"
                >
                  {d.value.toFixed(1)}
                </text>
              )}
              {/* Month label */}
              <text
                x={x + barW / 2} y={height + padB - 4}
                textAnchor="middle" fontSize={10} fill="#64748b"
              >
                {d.label}
              </text>
            </g>
          )
        })}

        <defs>
          <linearGradient id="barGrad" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0%" stopColor="#c81e1e" />
            <stop offset="100%" stopColor="#1a4b8c" />
          </linearGradient>
        </defs>
      </svg>
    </div>
  )
}

function DonutChart({ segments, size = 160 }) {
  const total = segments.reduce((s, d) => s + d.value, 0)
  if (!total) {
    return (
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', height: size, color: '#1e3a5a', fontSize: 13 }}>
        Нет данных
      </div>
    )
  }

  const R = size / 2 - 16
  const r = R * 0.58
  const cx = size / 2
  const cy = size / 2

  let angle = -Math.PI / 2
  const arcs = segments.filter(s => s.value > 0).map(seg => {
    const a = (seg.value / total) * 2 * Math.PI
    const x1 = cx + R * Math.cos(angle)
    const y1 = cy + R * Math.sin(angle)
    const x2 = cx + R * Math.cos(angle + a)
    const y2 = cy + R * Math.sin(angle + a)
    const ix1 = cx + r * Math.cos(angle + a)
    const iy1 = cy + r * Math.sin(angle + a)
    const ix2 = cx + r * Math.cos(angle)
    const iy2 = cy + r * Math.sin(angle)
    const large = a > Math.PI ? 1 : 0
    const path = `M${x1} ${y1} A${R} ${R} 0 ${large} 1 ${x2} ${y2} L${ix1} ${iy1} A${r} ${r} 0 ${large} 0 ${ix2} ${iy2} Z`
    angle += a
    return { ...seg, path }
  })

  return (
    <svg width={size} height={size}>
      {arcs.map((a, i) => (
        <path key={i} d={a.path} fill={a.color} />
      ))}
      <text x={cx} y={cy - 6} textAnchor="middle" fontSize={18} fontWeight="700" fill="#f1f5f9">
        {total}
      </text>
      <text x={cx} y={cy + 12} textAnchor="middle" fontSize={10} fill="#64748b">
        всего
      </text>
    </svg>
  )
}

const SCOPES = [
  { key: 'me', label: 'Мои данные', minRole: 'user', fn: getMyStatistics },
  { key: 'dept', label: 'Отдел', minRole: 'moderator', fn: getDepartmentStatistics },
  { key: 'org', label: 'Организация', minRole: 'admin', fn: getOrganizationStatistics },
  { key: 'all', label: 'Все', minRole: 'super_admin', fn: getAllStatistics },
]

export default function Statistics() {
  const { tokenData } = useAuth()
  const availableScopes = SCOPES.filter(s => hasRole(tokenData, s.minRole))
  const [activeScope, setActiveScope] = useState(availableScopes[0]?.key || 'me')
  const [stats, setStats] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    const scope = SCOPES.find(s => s.key === activeScope)
    if (!scope) return
    setLoading(true)
    setError(null)
    scope.fn()
      .then(r => setStats(r.data))
      .catch(e => setError(e.response?.data?.detail || 'Ошибка загрузки'))
      .finally(() => setLoading(false))
  }, [activeScope])

  const monthlyData = stats?.monthly_overtime_hours?.map(m => ({
    label: MONTHS_RU[m.month - 1] + '\'' + String(m.year).slice(2),
    value: m.hours,
  })) || []

  const donutSegments = [
    { label: 'Одобрено',  value: stats?.approved_day_offs || 0,  color: '#16a34a' },
    { label: 'Ожидает',   value: stats?.pending_day_offs || 0,   color: '#d97706' },
    { label: 'Отклонено', value: stats?.rejected_day_offs || 0,  color: '#c81e1e' },
  ]

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 20 }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', flexWrap: 'wrap', gap: 10 }}>
        <PageTitle>Статистика</PageTitle>

        {/* Scope selector */}
        {availableScopes.length > 1 && (
          <div style={{ display: 'flex', gap: 6 }}>
            {availableScopes.map(s => (
              <button
                key={s.key}
                onClick={() => setActiveScope(s.key)}
                style={{
                  background: activeScope === s.key ? 'rgba(200,30,30,0.15)' : 'transparent',
                  border: `1px solid ${activeScope === s.key ? '#c81e1e' : '#1e3a5a'}`,
                  borderRadius: 6,
                  padding: '5px 14px',
                  color: activeScope === s.key ? '#f87171' : '#94a3b8',
                  fontSize: 12,
                  fontWeight: activeScope === s.key ? 600 : 400,
                  cursor: 'pointer',
                  transition: 'all 0.15s',
                }}
              >
                {s.label}
              </button>
            ))}
          </div>
        )}
      </div>

      {loading && <Spinner />}
      {error && <div style={{ color: '#f87171', fontSize: 13 }}>{error}</div>}

      {!loading && !error && stats && (
        <>
          {/* Summary cards */}
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(160px, 1fr))', gap: 12 }}>
            <StatCard label="Переработок" value={stats.total_overtimes} sub="Всего записей" color="#c81e1e" />
            <StatCard
              label="Всего часов"
              value={`${stats.total_overtime_hours} ч`}
              sub="Суммарно"
              color="#1a4b8c"
            />
            <StatCard
              label="Доступно"
              value={`${stats.available_overtime_hours} ч`}
              sub="Для отгула"
              color="#16a34a"
            />
            <StatCard label="Отгулов" value={stats.total_day_offs} sub="Всего заявок" color="#d97706" />
          </div>

          {/* Charts row */}
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: 16 }}>
            {/* Bar chart - monthly hours */}
            <Card style={{ padding: 20 }}>
              <SectionTitle style={{ marginBottom: 4 }}>Переработки по месяцам</SectionTitle>
              <p style={{ color: '#64748b', fontSize: 11, margin: '0 0 16px' }}>Часов за каждый месяц</p>
              {monthlyData.length > 0 ? (
                <BarChart data={monthlyData} height={130} />
              ) : (
                <div style={{ color: '#1e3a5a', fontSize: 13, textAlign: 'center', padding: '30px 0' }}>
                  Нет данных
                </div>
              )}
            </Card>

            {/* Donut chart - day-off statuses */}
            <Card style={{ padding: 20 }}>
              <SectionTitle style={{ marginBottom: 4 }}>Статусы отгулов</SectionTitle>
              <p style={{ color: '#64748b', fontSize: 11, margin: '0 0 16px' }}>Распределение по статусам</p>
              <div style={{ display: 'flex', alignItems: 'center', gap: 20, flexWrap: 'wrap' }}>
                <DonutChart segments={donutSegments} size={150} />
                <div style={{ display: 'flex', flexDirection: 'column', gap: 10 }}>
                  {donutSegments.map(s => (
                    <div key={s.label} style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                      <div style={{ width: 10, height: 10, borderRadius: 2, background: s.color, flexShrink: 0 }} />
                      <span style={{ color: '#94a3b8', fontSize: 12 }}>{s.label}:</span>
                      <span style={{ color: '#f1f5f9', fontSize: 13, fontWeight: 600 }}>{s.value}</span>
                    </div>
                  ))}
                </div>
              </div>
            </Card>
          </div>

          {/* Detailed stats table */}
          <Card style={{ padding: 20 }}>
            <SectionTitle style={{ marginBottom: 16 }}>Детализация</SectionTitle>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: 12 }}>
              {[
                { label: 'Всего переработок', value: stats.total_overtimes, color: '#c81e1e' },
                { label: 'Часов накоплено', value: `${stats.total_overtime_hours} ч`, color: '#1a4b8c' },
                { label: 'Доступно для отгула', value: `${stats.available_overtime_hours} ч`, color: '#16a34a' },
                { label: 'Отгулов ожидает', value: stats.pending_day_offs, color: '#d97706' },
                { label: 'Отгулов одобрено', value: stats.approved_day_offs, color: '#16a34a' },
                { label: 'Отгулов отклонено', value: stats.rejected_day_offs, color: '#c81e1e' },
              ].map(item => (
                <div
                  key={item.label}
                  style={{
                    padding: '12px 14px',
                    background: '#0b1526',
                    borderRadius: 7,
                    borderLeft: `2px solid ${item.color}`,
                  }}
                >
                  <div style={{ color: '#64748b', fontSize: 11, marginBottom: 4 }}>{item.label}</div>
                  <div style={{ color: item.color, fontWeight: 700, fontSize: 20 }}>{item.value}</div>
                </div>
              ))}
            </div>
          </Card>
        </>
      )}
    </div>
  )
}
