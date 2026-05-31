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

// NavLink active style helper
const linkStyle = ({ isActive }) => ({
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
})

const mobileLinkStyle = ({ isActive }) => ({
  padding: '10px 14px',
  borderRadius: 8,
  fontSize: 14,
  fontWeight: isActive ? 600 : 400,
  textDecoration: 'none',
  color: isActive ? '#f1f5f9' : '#7a9bc2',
  background: isActive ? 'rgba(200,30,30,0.12)' : 'transparent',
  display: 'block',
})

export default function Navbar() {
  const navigate = useNavigate()
  const { tokenData, logout } = useAuth()
  const [menuOpen, setMenuOpen] = useState(false)

  const handleLogout = () => { logout(); navigate('/login') }

  const navLinks = [
    { to: '/dashboard',  label: 'Главная',     minRole: 'user' },
    { to: '/overtimes',  label: 'Переработки', minRole: 'user' },
    { to: '/day-offs',   label: 'Отгулы',      minRole: 'user' },
    { to: '/statistics', label: 'Статистика',  minRole: 'user' },
    { to: '/moderation', label: 'Отдел',       minRole: 'moderator' },
    { to: '/admin',      label: 'Управление',  minRole: 'admin' },
    { to: '/profile',    label: 'Профиль',     minRole: 'user' },
  ].filter(l => hasRole(tokenData, l.minRole))

  const roleColor = ROLE_COLORS[tokenData?.role] || '#60a5fa'

  return (
    <nav style={{
      position: 'sticky', top: 0, zIndex: 50,
      background: 'rgba(9,18,38,0.92)',
      backdropFilter: 'blur(12px)',
      WebkitBackdropFilter: 'blur(12px)',
      borderBottom: '1px solid rgba(40,80,130,0.25)',
      boxShadow: '0 1px 24px rgba(0,0,0,0.35)',
    }}>
      {/* Gradient accent line */}
      <div style={{ height: 2, background: 'linear-gradient(90deg,#c81e1e 0%,#a61818 30%,#1a4b8c 70%,#c81e1e 100%)' }} />

      <div className="navbar-inner">
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', height: 52 }}>

          {/* Logo */}
          <NavLink to="/dashboard" style={{ textDecoration: 'none', display: 'flex', alignItems: 'center', gap: 10 }}>
            <div style={{
              width: 34, height: 34, flexShrink: 0,
              background: 'linear-gradient(135deg, #c81e1e, #8b1010)',
              borderRadius: 8, display: 'flex', alignItems: 'center', justifyContent: 'center',
              fontWeight: 800, fontSize: 11, color: 'white',
              letterSpacing: '-0.5px', boxShadow: '0 2px 10px rgba(200,30,30,0.4)',
            }}>МЧС</div>
            <div className="logo-text">
              <div style={{ color: '#f1f5f9', fontWeight: 700, fontSize: 14, lineHeight: 1.2 }}>TimeKeep</div>
              <div style={{ color: '#4a6fa5', fontSize: 10 }}>МЧС Беларуси</div>
            </div>
          </NavLink>

          {/* Desktop nav — .nav-desktop shows/hides via CSS */}
          <div className="nav-desktop" style={{ display: 'flex', alignItems: 'center', gap: 2 }}>
            {navLinks.map(({ to, label }) => (
              <NavLink key={to} to={to} style={linkStyle}>{label}</NavLink>
            ))}
          </div>

          {/* Right */}
          <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
            {/* User info — .user-info shows via CSS */}
            {tokenData && (
              <div className="user-info" style={{ flexDirection: 'column', alignItems: 'flex-end' }}>
                <span style={{ color: '#c8d8ee', fontSize: 12, fontWeight: 600, lineHeight: 1.2 }}>
                  ID #{tokenData.user_id}
                </span>
                <span style={{ color: roleColor, fontSize: 10, fontWeight: 600, textTransform: 'uppercase', letterSpacing: '0.6px' }}>
                  {ROLE_LABELS[tokenData.role] || tokenData.role}
                </span>
              </div>
            )}

            <button onClick={handleLogout} className="logout-btn"
              style={{
                background: 'rgba(200,30,30,0.08)', border: '1px solid rgba(200,30,30,0.25)',
                borderRadius: 7, padding: '5px 14px',
                color: '#f87171', fontSize: 12, fontWeight: 600, cursor: 'pointer', transition: 'all 0.15s',
              }}
              onMouseEnter={e => { e.currentTarget.style.background = 'rgba(200,30,30,0.18)' }}
              onMouseLeave={e => { e.currentTarget.style.background = 'rgba(200,30,30,0.08)' }}
            >Выйти</button>

            {/* Burger — .nav-burger shows via CSS */}
            <button className="nav-burger"
              onClick={() => setMenuOpen(o => !o)}
              style={{
                background: menuOpen ? 'rgba(200,30,30,0.12)' : 'rgba(40,80,130,0.12)',
                border: `1px solid ${menuOpen ? 'rgba(200,30,30,0.3)' : 'rgba(40,80,130,0.25)'}`,
                borderRadius: 7, padding: '5px 9px',
                color: '#7a9bc2', cursor: 'pointer', fontSize: 16, lineHeight: 1,
                transition: 'all 0.15s',
              }}
            >{menuOpen ? '✕' : '☰'}</button>
          </div>
        </div>

        {/* Mobile dropdown */}
        {menuOpen && (
          <div style={{
            borderTop: '1px solid rgba(40,80,130,0.2)',
            padding: '8px 0 14px',
            display: 'flex', flexDirection: 'column', gap: 2,
          }}>
            {tokenData && (
              <div style={{ padding: '8px 14px 10px', borderBottom: '1px solid rgba(40,80,130,0.15)', marginBottom: 4 }}>
                <span style={{ color: '#c8d8ee', fontSize: 13, fontWeight: 600 }}>ID #{tokenData.user_id}</span>
                <span style={{ color: roleColor, fontSize: 11, fontWeight: 600, marginLeft: 10, textTransform: 'uppercase' }}>
                  {ROLE_LABELS[tokenData.role]}
                </span>
              </div>
            )}
            {navLinks.map(({ to, label }) => (
              <NavLink key={to} to={to}
                onClick={() => setMenuOpen(false)}
                style={mobileLinkStyle}
              >{label}</NavLink>
            ))}
          </div>
        )}
      </div>
    </nav>
  )
}
