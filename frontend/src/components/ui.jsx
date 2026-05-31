// Shared UI primitives — МЧС modern dark theme

const CARD_BG = 'linear-gradient(145deg, #112038 0%, #0d1b30 100%)'
const CARD_BORDER = 'rgba(42, 82, 132, 0.45)'
const CARD_SHADOW = '0 4px 20px rgba(0,0,0,0.3)'

export function Card({ children, style, className, hover = true }) {
  return (
    <div
      className={className}
      style={{
        background: CARD_BG,
        border: `1px solid ${CARD_BORDER}`,
        borderRadius: 12,
        boxShadow: CARD_SHADOW,
        transition: hover ? 'box-shadow 0.2s, transform 0.2s, border-color 0.2s' : undefined,
        ...style,
      }}
      onMouseEnter={hover ? e => {
        e.currentTarget.style.boxShadow = '0 8px 36px rgba(0,0,0,0.45), 0 0 0 1px rgba(40,80,130,0.35)'
        e.currentTarget.style.transform = 'translateY(-1px)'
        e.currentTarget.style.borderColor = 'rgba(42,82,132,0.7)'
      } : undefined}
      onMouseLeave={hover ? e => {
        e.currentTarget.style.boxShadow = CARD_SHADOW
        e.currentTarget.style.transform = 'none'
        e.currentTarget.style.borderColor = CARD_BORDER
      } : undefined}
    >
      {children}
    </div>
  )
}

export function PageTitle({ children }) {
  return (
    <h2 style={{ color: '#f1f5f9', fontWeight: 700, fontSize: 22, margin: 0, letterSpacing: '-0.3px' }}>
      {children}
    </h2>
  )
}

export function SectionTitle({ children, style }) {
  return (
    <h3 style={{ color: '#dde8f5', fontWeight: 600, fontSize: 14, margin: 0, letterSpacing: '0.1px', ...style }}>
      {children}
    </h3>
  )
}

export function Label({ children }) {
  return (
    <label style={{
      display: 'block', color: '#7a9bc2',
      fontSize: 11, marginBottom: 5, fontWeight: 600,
      textTransform: 'uppercase', letterSpacing: '0.6px',
    }}>
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
        background: 'rgba(8,15,30,0.7)',
        border: '1px solid rgba(42,82,132,0.4)',
        borderRadius: 7,
        padding: '8px 12px',
        fontSize: 13,
        color: '#e8f0fa',
        outline: 'none',
        transition: 'border-color 0.15s, box-shadow 0.15s',
        ...style,
      }}
      onFocus={e => {
        e.target.style.borderColor = 'rgba(200,30,30,0.7)'
        e.target.style.boxShadow = '0 0 0 3px rgba(200,30,30,0.08)'
      }}
      onBlur={e => {
        e.target.style.borderColor = 'rgba(42,82,132,0.4)'
        e.target.style.boxShadow = 'none'
      }}
    />
  )
}

export function Select({ children, style, ...props }) {
  return (
    <select
      {...props}
      style={{
        width: '100%',
        background: 'rgba(8,15,30,0.85)',
        border: '1px solid rgba(42,82,132,0.4)',
        borderRadius: 7,
        padding: '8px 12px',
        fontSize: 13,
        color: '#e8f0fa',
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
  const disabled = loading || props.disabled
  return (
    <button
      {...props}
      disabled={disabled}
      style={{
        background: disabled
          ? 'rgba(42,82,132,0.2)'
          : 'linear-gradient(135deg, #c81e1e 0%, #a61818 100%)',
        color: disabled ? '#4a6fa5' : 'white',
        border: 'none',
        borderRadius: 7,
        padding: '8px 20px',
        fontSize: 13, fontWeight: 600,
        cursor: disabled ? 'not-allowed' : 'pointer',
        transition: 'all 0.15s',
        boxShadow: disabled ? 'none' : '0 2px 12px rgba(200,30,30,0.35)',
        letterSpacing: '0.2px',
        ...style,
      }}
      onMouseEnter={e => { if (!disabled) { e.currentTarget.style.boxShadow = '0 4px 18px rgba(200,30,30,0.5)'; e.currentTarget.style.transform = 'translateY(-1px)' }}}
      onMouseLeave={e => { if (!disabled) { e.currentTarget.style.boxShadow = '0 2px 12px rgba(200,30,30,0.35)'; e.currentTarget.style.transform = 'none' }}}
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
        background: 'rgba(26,75,140,0.12)',
        color: '#93c5fd',
        border: '1px solid rgba(26,75,140,0.35)',
        borderRadius: 7,
        padding: '7px 18px',
        fontSize: 13, fontWeight: 500,
        cursor: 'pointer',
        transition: 'all 0.15s',
        ...style,
      }}
      onMouseEnter={e => { e.currentTarget.style.background = 'rgba(26,75,140,0.22)'; e.currentTarget.style.borderColor = 'rgba(26,75,140,0.6)' }}
      onMouseLeave={e => { e.currentTarget.style.background = 'rgba(26,75,140,0.12)'; e.currentTarget.style.borderColor = 'rgba(26,75,140,0.35)' }}
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
        background: 'rgba(200,30,30,0.08)',
        color: '#fca5a5',
        border: '1px solid rgba(200,30,30,0.2)',
        borderRadius: 6, padding: '4px 12px',
        fontSize: 12, cursor: 'pointer', transition: 'all 0.15s',
        ...style,
      }}
      onMouseEnter={e => { e.currentTarget.style.background = 'rgba(200,30,30,0.18)' }}
      onMouseLeave={e => { e.currentTarget.style.background = 'rgba(200,30,30,0.08)' }}
    >
      {children}
    </button>
  )
}

const STATUS_MAP = {
  pending:  { label: 'Ожидает',  bg: 'rgba(245,158,11,0.1)',  color: '#fcd34d', border: 'rgba(245,158,11,0.3)' },
  approved: { label: 'Одобрен',  bg: 'rgba(52,211,153,0.1)',  color: '#6ee7b7', border: 'rgba(52,211,153,0.3)' },
  rejected: { label: 'Отклонён', bg: 'rgba(248,113,113,0.1)', color: '#fca5a5', border: 'rgba(248,113,113,0.3)' },
  active:   { label: 'Активна',  bg: 'rgba(96,165,250,0.1)',  color: '#93c5fd', border: 'rgba(96,165,250,0.3)' },
  used:     { label: 'Списана',  bg: 'rgba(100,116,139,0.1)', color: '#94a3b8', border: 'rgba(100,116,139,0.3)' },
}

export function StatusBadge({ status }) {
  const s = STATUS_MAP[status] || { label: status, bg: 'rgba(42,82,132,0.15)', color: '#7a9bc2', border: 'rgba(42,82,132,0.3)' }
  return (
    <span style={{
      background: s.bg, color: s.color,
      border: `1px solid ${s.border}`,
      borderRadius: 20, padding: '2px 10px',
      fontSize: 11, fontWeight: 600, letterSpacing: '0.2px', whiteSpace: 'nowrap',
    }}>
      {s.label}
    </span>
  )
}

export function ErrorMsg({ children }) {
  if (!children) return null
  return (
    <div style={{
      background: 'rgba(200,30,30,0.07)',
      border: '1px solid rgba(200,30,30,0.2)',
      borderRadius: 7, padding: '9px 13px',
      color: '#fca5a5', fontSize: 12,
    }}>
      {children}
    </div>
  )
}

export function Divider() {
  return <div style={{ borderBottom: '1px solid rgba(42,82,132,0.25)', margin: '4px 0' }} />
}

export function Pagination({ offset, limit, onChangePage }) {
  const page = Math.floor(offset / limit) + 1
  const btnBase = {
    borderRadius: 6, padding: '5px 14px',
    fontSize: 12, cursor: 'pointer', transition: 'all 0.15s',
    fontWeight: 500,
  }
  return (
    <div style={{ display: 'flex', alignItems: 'center', gap: 10, justifyContent: 'flex-end', padding: '12px 16px', borderTop: '1px solid rgba(42,82,132,0.15)' }}>
      <button
        onClick={() => onChangePage(Math.max(0, offset - limit))}
        disabled={offset === 0}
        style={{
          ...btnBase,
          background: offset === 0 ? 'transparent' : 'rgba(42,82,132,0.12)',
          color: offset === 0 ? 'rgba(42,82,132,0.4)' : '#93c5fd',
          border: `1px solid ${offset === 0 ? 'rgba(42,82,132,0.15)' : 'rgba(42,82,132,0.3)'}`,
        }}
      >← Назад</button>

      <span style={{
        color: '#4a6fa5', fontSize: 12, fontWeight: 600,
        background: 'rgba(42,82,132,0.1)',
        border: '1px solid rgba(42,82,132,0.2)',
        borderRadius: 6, padding: '4px 12px',
      }}>
        {page}
      </span>

      <button
        onClick={() => onChangePage(offset + limit)}
        style={{
          ...btnBase,
          background: 'rgba(42,82,132,0.12)',
          color: '#93c5fd',
          border: '1px solid rgba(42,82,132,0.3)',
        }}
      >Вперёд →</button>
    </div>
  )
}

const STAT_GRADIENTS = {
  '#c81e1e': 'linear-gradient(135deg, rgba(200,30,30,0.12) 0%, rgba(200,30,30,0.04) 100%)',
  '#1a4b8c': 'linear-gradient(135deg, rgba(26,75,140,0.14) 0%, rgba(26,75,140,0.04) 100%)',
  '#16a34a': 'linear-gradient(135deg, rgba(22,163,74,0.12) 0%, rgba(22,163,74,0.04) 100%)',
  '#d97706': 'linear-gradient(135deg, rgba(217,119,6,0.12) 0%, rgba(217,119,6,0.04) 100%)',
}

export function StatCard({ label, value, sub, color = '#c81e1e' }) {
  const grad = STAT_GRADIENTS[color] || STAT_GRADIENTS['#c81e1e']
  return (
    <div style={{
      background: grad,
      border: `1px solid ${color}30`,
      borderRadius: 12,
      padding: '18px 22px',
      borderLeft: `3px solid ${color}`,
      boxShadow: `0 4px 20px rgba(0,0,0,0.2), 0 0 0 0 ${color}20`,
      transition: 'box-shadow 0.2s, transform 0.2s',
      cursor: 'default',
    }}
      onMouseEnter={e => {
        e.currentTarget.style.boxShadow = `0 8px 28px rgba(0,0,0,0.3), 0 0 12px ${color}18`
        e.currentTarget.style.transform = 'translateY(-2px)'
      }}
      onMouseLeave={e => {
        e.currentTarget.style.boxShadow = `0 4px 20px rgba(0,0,0,0.2), 0 0 0 0 ${color}20`
        e.currentTarget.style.transform = 'none'
      }}
    >
      <p style={{ color: '#7a9bc2', fontSize: 11, margin: '0 0 8px', textTransform: 'uppercase', letterSpacing: '0.7px', fontWeight: 600 }}>
        {label}
      </p>
      <p style={{ color: '#f0f7ff', fontWeight: 700, fontSize: 28, margin: 0, lineHeight: 1, letterSpacing: '-0.5px' }}>
        {value}
      </p>
      {sub && (
        <p style={{ color: '#4a6fa5', fontSize: 11, margin: '5px 0 0', fontWeight: 500 }}>{sub}</p>
      )}
    </div>
  )
}

export function TableContainer({ children }) {
  return (
    <div style={{
      background: 'linear-gradient(180deg, #0f1e36 0%, #0d1b30 100%)',
      border: `1px solid ${CARD_BORDER}`,
      borderRadius: 12,
      overflow: 'hidden',
      boxShadow: CARD_SHADOW,
    }}>
      {children}
    </div>
  )
}

export function Table({ children }) {
  return (
    <div style={{ overflowX: 'auto', WebkitOverflowScrolling: 'touch' }}>
      <table className="resp-table" style={{ width: '100%', borderCollapse: 'collapse', fontSize: 13, minWidth: 480 }}>
        {children}
      </table>
    </div>
  )
}

export function THead({ children }) {
  return (
    <thead>
      <tr style={{
        borderBottom: '1px solid rgba(42,82,132,0.3)',
        background: 'rgba(10,20,40,0.5)',
      }}>
        {children}
      </tr>
    </thead>
  )
}

export function Th({ children, style }) {
  return (
    <th style={{
      padding: '11px 18px',
      textAlign: 'left',
      color: '#4a6fa5',
      fontWeight: 700,
      fontSize: 10,
      textTransform: 'uppercase',
      letterSpacing: '0.8px',
      whiteSpace: 'nowrap',
      ...style,
    }}>
      {children}
    </th>
  )
}

export function Td({ children, style }) {
  return (
    <td style={{
      padding: '11px 18px',
      color: '#d0dff0',
      borderBottom: '1px solid rgba(30,58,90,0.3)',
      ...style,
    }}>
      {children}
    </td>
  )
}

export function TRow({ children, style }) {
  return (
    <tr
      style={{ transition: 'background 0.12s', ...style }}
      onMouseEnter={e => { e.currentTarget.style.background = 'rgba(26,75,140,0.08)' }}
      onMouseLeave={e => { e.currentTarget.style.background = 'transparent' }}
    >
      {children}
    </tr>
  )
}

export function EmptyState({ message = 'Нет записей' }) {
  return (
    <div style={{ padding: '48px 20px', textAlign: 'center' }}>
      <div style={{ fontSize: 32, marginBottom: 10, opacity: 0.15 }}>◈</div>
      <p style={{ color: '#3a5a7a', fontSize: 13, margin: 0, fontWeight: 500 }}>{message}</p>
    </div>
  )
}

export const MONTHS_RU = ['Янв','Фев','Мар','Апр','Май','Июн','Июл','Авг','Сен','Окт','Ноя','Дек']
