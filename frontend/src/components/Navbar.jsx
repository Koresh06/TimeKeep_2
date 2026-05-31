import { NavLink, useNavigate } from 'react-router-dom'
import { useAuth, hasRole } from '../context/AuthContext'
import { useState } from 'react'

const ROLE_LABELS = {
  user: 'Сотрудник',
  moderator: 'Модератор',
  admin: 'Администратор',
  super_admin: 'Суперадмин',
}

export default function Navbar() {
  const navigate = useNavigate()
  const { tokenData, logout } = useAuth()
  const [menuOpen, setMenuOpen] = useState(false)

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  const navLinks = [
    { to: '/dashboard', label: 'Главная', icon: '⊞', minRole: 'user' },
    { to: '/overtimes', label: 'Переработки', icon: '⏱', minRole: 'user' },
    { to: '/day-offs', label: 'Отгулы', icon: '📅', minRole: 'user' },
    { to: '/statistics', label: 'Статистика', icon: '📊', minRole: 'user' },
    { to: '/moderation', label: 'Отдел', icon: '🏢', minRole: 'moderator' },
    { to: '/admin', label: 'Управление', icon: '⚙', minRole: 'admin' },
    { to: '/profile', label: 'Профиль', icon: '👤', minRole: 'user' },
  ].filter(l => hasRole(tokenData, l.minRole))

  return (
    <nav
      style={{
        background: 'linear-gradient(135deg, #0b1526 0%, #0f1e36 100%)',
        borderBottom: '2px solid #c81e1e',
        position: 'sticky',
        top: 0,
        zIndex: 50,
      }}
    >
      {/* Red accent stripe at top */}
      <div style={{ height: '3px', background: 'linear-gradient(90deg, #c81e1e, #a61818 50%, #c81e1e)' }} />

      <div className="max-w-7xl mx-auto px-4 sm:px-6">
        <div className="flex items-center justify-between h-14">
          {/* Logo */}
          <NavLink to="/dashboard" className="flex items-center gap-3 no-underline">
            <div
              style={{
                width: 36,
                height: 36,
                background: '#c81e1e',
                borderRadius: 6,
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                fontWeight: 'bold',
                fontSize: 14,
                color: 'white',
                flexShrink: 0,
                letterSpacing: '-0.5px',
              }}
            >
              МЧС
            </div>
            <div className="hidden sm:block">
              <div style={{ color: '#f1f5f9', fontWeight: 700, fontSize: 15, lineHeight: 1.2 }}>
                TimeKeep
              </div>
              <div style={{ color: '#64748b', fontSize: 10 }}>Система учёта переработок</div>
            </div>
          </NavLink>

          {/* Desktop nav */}
          <div className="hidden md:flex items-center gap-1">
            {navLinks.map(({ to, label }) => (
              <NavLink
                key={to}
                to={to}
                style={({ isActive }) => ({
                  padding: '6px 12px',
                  borderRadius: 6,
                  fontSize: 13,
                  fontWeight: 500,
                  textDecoration: 'none',
                  color: isActive ? '#f1f5f9' : '#94a3b8',
                  background: isActive ? 'rgba(200,30,30,0.15)' : 'transparent',
                  borderBottom: isActive ? '2px solid #c81e1e' : '2px solid transparent',
                  transition: 'all 0.15s',
                })}
              >
                {label}
              </NavLink>
            ))}
          </div>

          {/* Right section */}
          <div className="flex items-center gap-3">
            {tokenData && (
              <div className="hidden sm:flex flex-col items-end">
                <span style={{ color: '#f1f5f9', fontSize: 12, fontWeight: 600 }}>
                  ID: {tokenData.user_id}
                </span>
                <span
                  style={{
                    color: '#c81e1e',
                    fontSize: 10,
                    fontWeight: 500,
                    textTransform: 'uppercase',
                    letterSpacing: '0.5px',
                  }}
                >
                  {ROLE_LABELS[tokenData.role] || tokenData.role}
                </span>
              </div>
            )}

            <button
              onClick={handleLogout}
              style={{
                background: 'rgba(200,30,30,0.1)',
                border: '1px solid rgba(200,30,30,0.3)',
                borderRadius: 6,
                padding: '5px 12px',
                color: '#c81e1e',
                fontSize: 12,
                fontWeight: 600,
                cursor: 'pointer',
                transition: 'all 0.15s',
                letterSpacing: '0.3px',
              }}
              onMouseEnter={e => {
                e.target.style.background = 'rgba(200,30,30,0.2)'
                e.target.style.borderColor = '#c81e1e'
              }}
              onMouseLeave={e => {
                e.target.style.background = 'rgba(200,30,30,0.1)'
                e.target.style.borderColor = 'rgba(200,30,30,0.3)'
              }}
            >
              Выйти
            </button>

            {/* Mobile menu toggle */}
            <button
              className="md:hidden"
              onClick={() => setMenuOpen(!menuOpen)}
              style={{
                background: 'transparent',
                border: '1px solid #1e3a5a',
                borderRadius: 6,
                padding: '5px 8px',
                color: '#94a3b8',
                cursor: 'pointer',
                fontSize: 16,
              }}
            >
              ☰
            </button>
          </div>
        </div>

        {/* Mobile menu */}
        {menuOpen && (
          <div
            className="md:hidden pb-3 flex flex-col gap-1"
            style={{ borderTop: '1px solid #1e3a5a' }}
          >
            {navLinks.map(({ to, label, icon }) => (
              <NavLink
                key={to}
                to={to}
                onClick={() => setMenuOpen(false)}
                style={({ isActive }) => ({
                  padding: '8px 12px',
                  borderRadius: 6,
                  fontSize: 13,
                  fontWeight: 500,
                  textDecoration: 'none',
                  color: isActive ? '#f1f5f9' : '#94a3b8',
                  background: isActive ? 'rgba(200,30,30,0.15)' : 'transparent',
                  display: 'flex',
                  alignItems: 'center',
                  gap: 8,
                })}
              >
                <span>{icon}</span>
                {label}
              </NavLink>
            ))}
          </div>
        )}
      </div>
    </nav>
  )
}
