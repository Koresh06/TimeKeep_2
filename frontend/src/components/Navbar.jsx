import { NavLink, useNavigate } from 'react-router-dom'
import { useAuth, hasRole } from '../context/AuthContext'
import { useState } from 'react'

const ROLE_LABELS = {
  user: 'Сотрудник',
  moderator: 'Модератор',
  admin: 'Администратор',
  super_admin: 'Суперадмин',
}

const ROLE_COLORS = {
  user: '#60a5fa',
  moderator: '#34d399',
  admin: '#fbbf24',
  super_admin: '#f87171',
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
    { to: '/dashboard',  label: 'Главная',      minRole: 'user' },
    { to: '/overtimes',  label: 'Переработки',  minRole: 'user' },
    { to: '/day-offs',   label: 'Отгулы',       minRole: 'user' },
    { to: '/statistics', label: 'Статистика',   minRole: 'user' },
    { to: '/moderation', label: 'Отдел',        minRole: 'moderator' },
    { to: '/admin',      label: 'Управление',   minRole: 'admin' },
    { to: '/profile',    label: 'Профиль',      minRole: 'user' },
  ].filter(l => hasRole(tokenData, l.minRole))

  const roleColor = ROLE_COLORS[tokenData?.role] || '#60a5fa'

  return (
    <nav
      style={{
        position: 'sticky',
        top: 0,
        zIndex: 50,
        background: 'rgba(9, 18, 38, 0.92)',
        backdropFilter: 'blur(12px)',
        WebkitBackdropFilter: 'blur(12px)',
        borderBottom: '1px solid rgba(40, 80, 130, 0.25)',
        boxShadow: '0 1px 24px rgba(0,0,0,0.35)',
      }}
    >
      {/* Gradient top accent line */}
      <div style={{
        height: 2,
        background: 'linear-gradient(90deg, #c81e1e 0%, #a61818 30%, #1a4b8c 70%, #c81e1e 100%)',
        opacity: 0.9,
      }} />

      <div style={{ maxWidth: 1520, margin: '0 auto', padding: '0 32px' }}>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', height: 52 }}>

          {/* Logo */}
          <NavLink to="/dashboard" style={{ textDecoration: 'none', display: 'flex', alignItems: 'center', gap: 12 }}>
            <div style={{
              width: 34, height: 34,
              background: 'linear-gradient(135deg, #c81e1e 0%, #8b1010 100%)',
              borderRadius: 8,
              display: 'flex', alignItems: 'center', justifyContent: 'center',
              fontWeight: 800, fontSize: 11, color: 'white',
              letterSpacing: '-0.5px',
              boxShadow: '0 2px 10px rgba(200,30,30,0.4)',
              flexShrink: 0,
            }}>МЧС</div>
            <div style={{ display: 'none' }} className="sm:block">
              <div style={{ color: '#f1f5f9', fontWeight: 700, fontSize: 14, lineHeight: 1.2, letterSpacing: '0.2px' }}>
                TimeKeep
              </div>
              <div style={{ color: '#4a6fa5', fontSize: 10, letterSpacing: '0.3px' }}>
                МЧС Беларуси
              </div>
            </div>
          </NavLink>

          {/* Desktop nav */}
          <div style={{ display: 'none', alignItems: 'center', gap: 2 }} className="md:flex">
            {navLinks.map(({ to, label }) => (
              <NavLink
                key={to}
                to={to}
                style={({ isActive }) => ({
                  padding: '5px 13px',
                  borderRadius: 7,
                  fontSize: 13,
                  fontWeight: 500,
                  textDecoration: 'none',
                  color: isActive ? '#f1f5f9' : '#7a9bc2',
                  background: isActive
                    ? 'linear-gradient(135deg, rgba(200,30,30,0.18) 0%, rgba(26,75,140,0.12) 100%)'
                    : 'transparent',
                  border: isActive ? '1px solid rgba(200,30,30,0.3)' : '1px solid transparent',
                  transition: 'all 0.15s',
                  whiteSpace: 'nowrap',
                })}
              >
                {label}
              </NavLink>
            ))}
          </div>

          {/* Right section */}
          <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
            {tokenData && (
              <div style={{ display: 'none', flexDirection: 'column', alignItems: 'flex-end' }} className="sm:flex">
                <span style={{ color: '#c8d8ee', fontSize: 12, fontWeight: 600, lineHeight: 1.2 }}>
                  ID #{tokenData.user_id}
                </span>
                <span style={{
                  color: roleColor,
                  fontSize: 10, fontWeight: 600,
                  textTransform: 'uppercase', letterSpacing: '0.6px',
                }}>
                  {ROLE_LABELS[tokenData.role] || tokenData.role}
                </span>
              </div>
            )}

            <button
              onClick={handleLogout}
              style={{
                background: 'rgba(200,30,30,0.08)',
                border: '1px solid rgba(200,30,30,0.25)',
                borderRadius: 7,
                padding: '5px 14px',
                color: '#f87171',
                fontSize: 12, fontWeight: 600,
                cursor: 'pointer',
                transition: 'all 0.15s',
                letterSpacing: '0.2px',
              }}
              onMouseEnter={e => {
                e.currentTarget.style.background = 'rgba(200,30,30,0.18)'
                e.currentTarget.style.borderColor = 'rgba(200,30,30,0.5)'
              }}
              onMouseLeave={e => {
                e.currentTarget.style.background = 'rgba(200,30,30,0.08)'
                e.currentTarget.style.borderColor = 'rgba(200,30,30,0.25)'
              }}
            >
              Выйти
            </button>

            {/* Mobile menu */}
            <button
              className="md:hidden"
              onClick={() => setMenuOpen(!menuOpen)}
              style={{
                background: 'rgba(40,80,130,0.15)',
                border: '1px solid rgba(40,80,130,0.3)',
                borderRadius: 7, padding: '5px 9px',
                color: '#7a9bc2', cursor: 'pointer', fontSize: 16,
              }}
            >☰</button>
          </div>
        </div>

        {/* Mobile dropdown */}
        {menuOpen && (
          <div style={{ borderTop: '1px solid rgba(40,80,130,0.2)', paddingBottom: 12, display: 'flex', flexDirection: 'column', gap: 2 }}
            className="md:hidden">
            {navLinks.map(({ to, label }) => (
              <NavLink key={to} to={to}
                onClick={() => setMenuOpen(false)}
                style={({ isActive }) => ({
                  padding: '9px 12px', borderRadius: 7, fontSize: 13,
                  fontWeight: isActive ? 600 : 400, textDecoration: 'none',
                  color: isActive ? '#f1f5f9' : '#7a9bc2',
                  background: isActive ? 'rgba(200,30,30,0.15)' : 'transparent',
                })}
              >{label}</NavLink>
            ))}
          </div>
        )}
      </div>
    </nav>
  )
}
