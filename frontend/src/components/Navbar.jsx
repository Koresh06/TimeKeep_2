import { NavLink, useNavigate } from 'react-router-dom'

const links = [
  { to: '/dashboard', label: 'Главная' },
  { to: '/overtimes', label: 'Переработки' },
  { to: '/day-offs', label: 'Отгулы' },
  { to: '/profile', label: 'Профиль' },
]

export default function Navbar() {
  const navigate = useNavigate()

  const logout = () => {
    localStorage.removeItem('token')
    navigate('/login')
  }

  return (
    <nav className="bg-slate-900 border-b border-slate-700 px-6 py-3 flex items-center justify-between">
      <span className="text-blue-400 font-bold text-lg tracking-wide">TimeKeep</span>
      <div className="flex gap-6 items-center">
        {links.map(({ to, label }) => (
          <NavLink
            key={to}
            to={to}
            className={({ isActive }) =>
              `text-sm font-medium transition-colors ${
                isActive ? 'text-blue-400' : 'text-slate-400 hover:text-slate-200'
              }`
            }
          >
            {label}
          </NavLink>
        ))}
        <button
          onClick={logout}
          className="text-sm text-slate-400 hover:text-red-400 transition-colors ml-4"
        >
          Выйти
        </button>
      </div>
    </nav>
  )
}
