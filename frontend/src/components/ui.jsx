// Shared UI primitives for МЧС theme

export function Card({ children, style, className }) {
  return (
    <div
      className={className}
      style={{
        background: '#0f1e36',
        border: '1px solid #1e3a5a',
        borderRadius: 10,
        ...style,
      }}
    >
      {children}
    </div>
  )
}

export function PageTitle({ children }) {
  return (
    <h2 style={{ color: '#f1f5f9', fontWeight: 700, fontSize: 22, margin: 0 }}>
      {children}
    </h2>
  )
}

export function SectionTitle({ children }) {
  return (
    <h3 style={{ color: '#e2e8f0', fontWeight: 600, fontSize: 15, margin: 0 }}>
      {children}
    </h3>
  )
}

export function Label({ children }) {
  return (
    <label style={{ display: 'block', color: '#94a3b8', fontSize: 11, marginBottom: 4, fontWeight: 500, textTransform: 'uppercase', letterSpacing: '0.5px' }}>
      {children}
    </label>
  )
}

export function Input({ style, ...props }) {
  return (
    <input
      {...props}
      style={{
        width: '100%',
        background: '#0b1526',
        border: '1px solid #1e3a5a',
        borderRadius: 6,
        padding: '7px 10px',
        fontSize: 13,
        color: '#f1f5f9',
        outline: 'none',
        transition: 'border-color 0.15s',
        ...style,
      }}
      onFocus={e => { e.target.style.borderColor = '#c81e1e' }}
      onBlur={e => { e.target.style.borderColor = '#1e3a5a' }}
    />
  )
}

export function Select({ children, style, ...props }) {
  return (
    <select
      {...props}
      style={{
        width: '100%',
        background: '#0b1526',
        border: '1px solid #1e3a5a',
        borderRadius: 6,
        padding: '7px 10px',
        fontSize: 13,
        color: '#f1f5f9',
        outline: 'none',
        cursor: 'pointer',
        ...style,
      }}
    >
      {children}
    </select>
  )
}

export function BtnPrimary({ children, style, loading, ...props }) {
  return (
    <button
      {...props}
      disabled={loading || props.disabled}
      style={{
        background: loading || props.disabled ? '#1e3a5a' : '#c81e1e',
        color: 'white',
        border: 'none',
        borderRadius: 6,
        padding: '8px 18px',
        fontSize: 13,
        fontWeight: 600,
        cursor: loading || props.disabled ? 'not-allowed' : 'pointer',
        transition: 'background 0.15s',
        ...style,
      }}
      onMouseEnter={e => { if (!loading && !props.disabled) e.currentTarget.style.background = '#a61818' }}
      onMouseLeave={e => { if (!loading && !props.disabled) e.currentTarget.style.background = '#c81e1e' }}
    >
      {loading ? 'Загрузка...' : children}
    </button>
  )
}

export function BtnSecondary({ children, style, ...props }) {
  return (
    <button
      {...props}
      style={{
        background: 'rgba(26,75,140,0.15)',
        color: '#93c5fd',
        border: '1px solid rgba(26,75,140,0.4)',
        borderRadius: 6,
        padding: '7px 16px',
        fontSize: 13,
        fontWeight: 500,
        cursor: 'pointer',
        transition: 'all 0.15s',
        ...style,
      }}
      onMouseEnter={e => { e.currentTarget.style.background = 'rgba(26,75,140,0.25)' }}
      onMouseLeave={e => { e.currentTarget.style.background = 'rgba(26,75,140,0.15)' }}
    >
      {children}
    </button>
  )
}

export function BtnDanger({ children, style, ...props }) {
  return (
    <button
      {...props}
      style={{
        background: 'rgba(200,30,30,0.1)',
        color: '#fca5a5',
        border: '1px solid rgba(200,30,30,0.25)',
        borderRadius: 6,
        padding: '5px 12px',
        fontSize: 12,
        cursor: 'pointer',
        transition: 'all 0.15s',
        ...style,
      }}
      onMouseEnter={e => { e.currentTarget.style.background = 'rgba(200,30,30,0.2)' }}
      onMouseLeave={e => { e.currentTarget.style.background = 'rgba(200,30,30,0.1)' }}
    >
      {children}
    </button>
  )
}

const STATUS_MAP = {
  pending:  { label: 'Ожидает',   bg: 'rgba(245,158,11,0.12)', color: '#fbbf24', border: 'rgba(245,158,11,0.3)' },
  approved: { label: 'Одобрен',   bg: 'rgba(34,197,94,0.1)',   color: '#4ade80', border: 'rgba(34,197,94,0.3)' },
  rejected: { label: 'Отклонён',  bg: 'rgba(239,68,68,0.1)',   color: '#f87171', border: 'rgba(239,68,68,0.3)' },
  active:   { label: 'Активна',   bg: 'rgba(96,165,250,0.1)',  color: '#93c5fd', border: 'rgba(96,165,250,0.3)' },
  used:     { label: 'Списана',   bg: 'rgba(100,116,139,0.1)', color: '#94a3b8', border: 'rgba(100,116,139,0.3)' },
}

export function StatusBadge({ status }) {
  const s = STATUS_MAP[status] || { label: status, bg: '#1e3a5a', color: '#94a3b8', border: '#1e3a5a' }
  return (
    <span
      style={{
        background: s.bg,
        color: s.color,
        border: `1px solid ${s.border}`,
        borderRadius: 20,
        padding: '2px 10px',
        fontSize: 11,
        fontWeight: 600,
        letterSpacing: '0.3px',
        whiteSpace: 'nowrap',
      }}
    >
      {s.label}
    </span>
  )
}

export function ErrorMsg({ children }) {
  if (!children) return null
  return (
    <div
      style={{
        background: 'rgba(200,30,30,0.08)',
        border: '1px solid rgba(200,30,30,0.25)',
        borderRadius: 6,
        padding: '8px 12px',
        color: '#fca5a5',
        fontSize: 12,
      }}
    >
      {children}
    </div>
  )
}

export function Divider() {
  return <div style={{ borderBottom: '1px solid #1e3a5a', margin: '4px 0' }} />
}

// Pagination component
export function Pagination({ offset, limit, total, onChangePage }) {
  const page = Math.floor(offset / limit) + 1
  const totalPages = total !== undefined ? Math.ceil(total / limit) : null

  return (
    <div style={{ display: 'flex', alignItems: 'center', gap: 8, justifyContent: 'flex-end', padding: '12px 16px' }}>
      <button
        onClick={() => onChangePage(Math.max(0, offset - limit))}
        disabled={offset === 0}
        style={{
          background: offset === 0 ? '#0f1e36' : 'rgba(26,75,140,0.15)',
          color: offset === 0 ? '#1e3a5a' : '#93c5fd',
          border: '1px solid #1e3a5a',
          borderRadius: 5,
          padding: '4px 10px',
          fontSize: 12,
          cursor: offset === 0 ? 'not-allowed' : 'pointer',
        }}
      >
        ← Назад
      </button>
      <span style={{ color: '#64748b', fontSize: 12 }}>
        Стр. {page}{totalPages ? ` / ${totalPages}` : ''}
      </span>
      <button
        onClick={() => onChangePage(offset + limit)}
        style={{
          background: 'rgba(26,75,140,0.15)',
          color: '#93c5fd',
          border: '1px solid #1e3a5a',
          borderRadius: 5,
          padding: '4px 10px',
          fontSize: 12,
          cursor: 'pointer',
        }}
      >
        Вперёд →
      </button>
    </div>
  )
}

// Stat card
export function StatCard({ label, value, sub, color = '#c81e1e' }) {
  return (
    <div
      style={{
        background: '#0f1e36',
        border: '1px solid #1e3a5a',
        borderRadius: 10,
        padding: '18px 20px',
        borderLeft: `3px solid ${color}`,
      }}
    >
      <p style={{ color: '#64748b', fontSize: 11, margin: '0 0 6px', textTransform: 'uppercase', letterSpacing: '0.5px' }}>
        {label}
      </p>
      <p style={{ color: '#f1f5f9', fontWeight: 700, fontSize: 26, margin: 0, lineHeight: 1 }}>
        {value}
      </p>
      {sub && (
        <p style={{ color: '#64748b', fontSize: 11, margin: '4px 0 0' }}>{sub}</p>
      )}
    </div>
  )
}

export function TableContainer({ children }) {
  return (
    <div style={{
      background: '#0f1e36',
      border: '1px solid #1e3a5a',
      borderRadius: 10,
      overflow: 'hidden',
    }}>
      {children}
    </div>
  )
}

export function Table({ children }) {
  return (
    <div style={{ overflowX: 'auto' }}>
      <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: 13 }}>
        {children}
      </table>
    </div>
  )
}

export function THead({ children }) {
  return (
    <thead>
      <tr style={{ borderBottom: '1px solid #1e3a5a' }}>
        {children}
      </tr>
    </thead>
  )
}

export function Th({ children, style }) {
  return (
    <th
      style={{
        padding: '10px 16px',
        textAlign: 'left',
        color: '#64748b',
        fontWeight: 600,
        fontSize: 10,
        textTransform: 'uppercase',
        letterSpacing: '0.5px',
        whiteSpace: 'nowrap',
        ...style,
      }}
    >
      {children}
    </th>
  )
}

export function Td({ children, style }) {
  return (
    <td
      style={{
        padding: '10px 16px',
        color: '#e2e8f0',
        borderBottom: '1px solid rgba(30,58,90,0.5)',
        ...style,
      }}
    >
      {children}
    </td>
  )
}

export function TRow({ children, style }) {
  return (
    <tr
      style={{
        transition: 'background 0.1s',
        ...style,
      }}
      onMouseEnter={e => { e.currentTarget.style.background = 'rgba(30,58,90,0.3)' }}
      onMouseLeave={e => { e.currentTarget.style.background = 'transparent' }}
    >
      {children}
    </tr>
  )
}

export function EmptyState({ message = 'Нет записей' }) {
  return (
    <div style={{ padding: '40px 20px', textAlign: 'center', color: '#1e3a5a' }}>
      <div style={{ fontSize: 36, marginBottom: 8 }}>—</div>
      <p style={{ color: '#64748b', fontSize: 13, margin: 0 }}>{message}</p>
    </div>
  )
}

// Month name helper
export const MONTHS_RU = ['Янв','Фев','Мар','Апр','Май','Июн','Июл','Авг','Сен','Окт','Ноя','Дек']
