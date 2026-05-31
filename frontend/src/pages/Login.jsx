import { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { login } from '../api/auth'
import { useAuth } from '../context/AuthContext'
import { Input, Label, BtnPrimary, ErrorMsg } from '../components/ui'

export default function Login() {
  const navigate = useNavigate()
  const { saveToken } = useAuth()
  const [form, setForm] = useState({ username: '', password: '' })
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    setLoading(true)
    try {
      const res = await login(form.username, form.password)
      saveToken(res.data.access_token)
      navigate('/dashboard')
    } catch (e) {
      setError(e.response?.data?.detail || 'Неверный логин или пароль')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div
      style={{
        minHeight: '100vh',
        background: 'linear-gradient(160deg, #060e1e 0%, #0b1526 50%, #060e1e 100%)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        padding: '24px 16px',
      }}
    >
      <div style={{ width: '100%', maxWidth: 400 }}>
        {/* Header badge */}
        <div style={{ textAlign: 'center', marginBottom: 32 }}>
          <div
            style={{
              display: 'inline-flex',
              alignItems: 'center',
              justifyContent: 'center',
              width: 64,
              height: 64,
              background: 'linear-gradient(135deg, #c81e1e, #a61818)',
              borderRadius: 14,
              fontSize: 20,
              fontWeight: 800,
              color: 'white',
              marginBottom: 16,
              boxShadow: '0 8px 32px rgba(200,30,30,0.3)',
              letterSpacing: '-1px',
            }}
          >
            МЧС
          </div>
          <h1 style={{ color: '#f1f5f9', fontWeight: 700, fontSize: 22, margin: '0 0 4px' }}>
            TimeKeep
          </h1>
          <p style={{ color: '#64748b', fontSize: 12, margin: 0 }}>
            Система учёта переработок МЧС Беларуси
          </p>
        </div>

        {/* Card */}
        <div
          style={{
            background: '#0f1e36',
            border: '1px solid #1e3a5a',
            borderRadius: 12,
            padding: '24px 20px',
            boxShadow: '0 20px 60px rgba(0,0,0,0.4)',
          }}
        >
          <div style={{ display: 'flex', gap: 0, marginBottom: 24, borderBottom: '1px solid #1e3a5a' }}>
            <span style={{ color: '#c81e1e', fontWeight: 600, fontSize: 14, paddingBottom: 10, borderBottom: '2px solid #c81e1e', marginBottom: -1 }}>
              Вход
            </span>
          </div>

          <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>
            <div>
              <Label>Логин</Label>
              <Input
                type="text"
                value={form.username}
                onChange={e => setForm({ ...form, username: e.target.value })}
                required
                placeholder="Введите логин"
              />
            </div>
            <div>
              <Label>Пароль</Label>
              <Input
                type="password"
                value={form.password}
                onChange={e => setForm({ ...form, password: e.target.value })}
                required
                placeholder="Введите пароль"
              />
            </div>

            <ErrorMsg>{error}</ErrorMsg>

            <BtnPrimary type="submit" loading={loading} style={{ width: '100%', padding: '10px', marginTop: 4 }}>
              Войти в систему
            </BtnPrimary>
          </form>

          <div style={{ textAlign: 'center', marginTop: 16 }}>
            <span style={{ color: '#64748b', fontSize: 12 }}>Нет аккаунта? </span>
            <Link
              to="/register"
              style={{ color: '#93c5fd', fontSize: 12, textDecoration: 'none', fontWeight: 500 }}
            >
              Зарегистрироваться
            </Link>
          </div>
        </div>

        <p style={{ textAlign: 'center', color: '#1e3a5a', fontSize: 10, marginTop: 20 }}>
          МЧС Республики Беларусь · Система учёта рабочего времени
        </p>
      </div>
    </div>
  )
}
