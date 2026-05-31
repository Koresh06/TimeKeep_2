import { useState, useEffect } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { register, getPublicOrganizations, getPublicDepartments } from '../api/auth'
import { Input, Label, Select, BtnPrimary, ErrorMsg } from '../components/ui'

const RANKS = [
  { value: 'рядовой внутренней службы', label: 'Рядовой' },
  { value: 'младший сержант внутренней службы', label: 'Мл. сержант' },
  { value: 'сержант внутренней службы', label: 'Сержант' },
  { value: 'старший сержант внутренней службы', label: 'Ст. сержант' },
  { value: 'старшина внутренней службы', label: 'Старшина' },
  { value: 'прапорщик внутренней службы', label: 'Прапорщик' },
  { value: 'старший прапорщик внутренней службы', label: 'Ст. прапорщик' },
  { value: 'лейтенант внутренней службы', label: 'Лейтенант' },
  { value: 'старший лейтенант внутренней службы', label: 'Ст. лейтенант' },
  { value: 'капитан внутренней службы', label: 'Капитан' },
  { value: 'майор внутренней службы', label: 'Майор' },
  { value: 'подполковник внутренней службы', label: 'Подполковник' },
  { value: 'полковник внутренней службы', label: 'Полковник' },
  { value: 'генерал-майор внутренней службы', label: 'Генерал-майор' },
  { value: 'генерал-лейтенант внутренней службы', label: 'Генерал-лейтенант' },
  { value: 'генерал-полковник внутренней службы', label: 'Генерал-полковник' },
]

const empty = {
  login: '', password: '', confirmPassword: '',
  surname: '', first_name: '', patronymic: '',
  position: '', rank: RANKS[7].value, work_mode: 'daily',
  organization_id: '', department_id: '',
}

export default function Register() {
  const navigate = useNavigate()
  const [form, setForm] = useState(empty)
  const [orgs, setOrgs] = useState([])
  const [depts, setDepts] = useState([])
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const [step, setStep] = useState(1)

  useEffect(() => {
    getPublicOrganizations()
      .then(r => setOrgs(r.data || []))
      .catch(() => setOrgs([]))
  }, [])

  useEffect(() => {
    if (!form.organization_id) { setDepts([]); return }
    getPublicDepartments(form.organization_id)
      .then(r => setDepts(r.data || []))
      .catch(() => setDepts([]))
  }, [form.organization_id])

  const set = (k) => (e) => setForm(f => ({ ...f, [k]: e.target.value }))

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    if (form.password !== form.confirmPassword) {
      setError('Пароли не совпадают')
      return
    }
    setLoading(true)
    try {
      await register({
        login: form.login,
        password: form.password,
        surname: form.surname,
        first_name: form.first_name,
        patronymic: form.patronymic,
        position: form.position,
        rank: form.rank,
        work_mode: form.work_mode,
        organization_id: parseInt(form.organization_id),
        department_id: parseInt(form.department_id),
      })
      navigate('/login', { state: { registered: true } })
    } catch (e) {
      setError(e.response?.data?.detail || 'Ошибка при регистрации')
    } finally {
      setLoading(false)
    }
  }

  const inputStyle = {
    width: '100%',
    background: '#0b1526',
    border: '1px solid #1e3a5a',
    borderRadius: 6,
    padding: '7px 10px',
    fontSize: 13,
    color: '#f1f5f9',
    outline: 'none',
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
      <div style={{ width: '100%', maxWidth: 520 }}>
        <div style={{ textAlign: 'center', marginBottom: 24 }}>
          <div
            style={{
              display: 'inline-flex',
              alignItems: 'center',
              justifyContent: 'center',
              width: 52,
              height: 52,
              background: 'linear-gradient(135deg, #c81e1e, #a61818)',
              borderRadius: 12,
              fontSize: 16,
              fontWeight: 800,
              color: 'white',
              marginBottom: 12,
              boxShadow: '0 8px 24px rgba(200,30,30,0.25)',
            }}
          >
            МЧС
          </div>
          <h1 style={{ color: '#f1f5f9', fontWeight: 700, fontSize: 20, margin: '0 0 4px' }}>
            Регистрация
          </h1>
          <p style={{ color: '#64748b', fontSize: 12, margin: 0 }}>TimeKeep · МЧС Беларуси</p>
        </div>

        <div
          style={{
            background: '#0f1e36',
            border: '1px solid #1e3a5a',
            borderRadius: 12,
            padding: '24px',
            boxShadow: '0 20px 60px rgba(0,0,0,0.4)',
          }}
        >
          {/* Steps indicator */}
          <div style={{ display: 'flex', gap: 0, marginBottom: 24, borderBottom: '1px solid #1e3a5a' }}>
            {[1, 2, 3].map(s => (
              <button
                key={s}
                type="button"
                onClick={() => setStep(s)}
                style={{
                  flex: 1,
                  background: 'transparent',
                  border: 'none',
                  borderBottom: step === s ? '2px solid #c81e1e' : '2px solid transparent',
                  padding: '0 0 10px',
                  marginBottom: -1,
                  color: step === s ? '#f1f5f9' : '#64748b',
                  fontSize: 12,
                  fontWeight: step === s ? 600 : 400,
                  cursor: 'pointer',
                }}
              >
                {s === 1 ? 'Учётные данные' : s === 2 ? 'Личные данные' : 'Подразделение'}
              </button>
            ))}
          </div>

          <form onSubmit={handleSubmit}>
            {/* Step 1: credentials */}
            {step === 1 && (
              <div style={{ display: 'flex', flexDirection: 'column', gap: 14 }}>
                <div>
                  <Label>Логин</Label>
                  <Input value={form.login} onChange={set('login')} required placeholder="Уникальный логин" />
                </div>
                <div>
                  <Label>Пароль</Label>
                  <Input type="password" value={form.password} onChange={set('password')} required placeholder="Минимум 6 символов" />
                </div>
                <div>
                  <Label>Подтверждение пароля</Label>
                  <Input type="password" value={form.confirmPassword} onChange={set('confirmPassword')} required placeholder="Повторите пароль" />
                </div>
                <button
                  type="button"
                  onClick={() => setStep(2)}
                  disabled={!form.login || !form.password || !form.confirmPassword}
                  style={{
                    background: form.login && form.password && form.confirmPassword ? '#c81e1e' : '#1e3a5a',
                    color: 'white',
                    border: 'none',
                    borderRadius: 6,
                    padding: '9px',
                    fontSize: 13,
                    fontWeight: 600,
                    cursor: form.login && form.password && form.confirmPassword ? 'pointer' : 'not-allowed',
                    marginTop: 4,
                  }}
                >
                  Далее →
                </button>
              </div>
            )}

            {/* Step 2: personal data */}
            {step === 2 && (
              <div style={{ display: 'flex', flexDirection: 'column', gap: 14 }}>
                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(130px, 1fr))', gap: 10 }}>
                  <div>
                    <Label>Фамилия</Label>
                    <Input value={form.surname} onChange={set('surname')} required placeholder="Иванов" />
                  </div>
                  <div>
                    <Label>Имя</Label>
                    <Input value={form.first_name} onChange={set('first_name')} required placeholder="Иван" />
                  </div>
                </div>
                <div>
                  <Label>Отчество</Label>
                  <Input value={form.patronymic} onChange={set('patronymic')} required placeholder="Иванович" />
                </div>
                <div>
                  <Label>Должность</Label>
                  <Input value={form.position} onChange={set('position')} required placeholder="Специалист / Инспектор" />
                </div>
                <div>
                  <Label>Воинское звание</Label>
                  <Select value={form.rank} onChange={set('rank')}>
                    {RANKS.map(r => (
                      <option key={r.value} value={r.value}>{r.label}</option>
                    ))}
                  </Select>
                </div>
                <div>
                  <Label>Режим работы</Label>
                  <Select value={form.work_mode} onChange={set('work_mode')}>
                    <option value="daily">Ежедневный (8 ч / отгул)</option>
                    <option value="shift">Сменный (24 ч / отгул)</option>
                  </Select>
                </div>
                <div style={{ display: 'flex', gap: 8, marginTop: 4 }}>
                  <button type="button" onClick={() => setStep(1)}
                    style={{ flex: 1, background: '#0b1526', color: '#94a3b8', border: '1px solid #1e3a5a', borderRadius: 6, padding: '8px', fontSize: 12, cursor: 'pointer' }}>
                    ← Назад
                  </button>
                  <button type="button" onClick={() => setStep(3)}
                    disabled={!form.surname || !form.first_name || !form.patronymic || !form.position}
                    style={{ flex: 2, background: form.surname && form.first_name && form.patronymic && form.position ? '#c81e1e' : '#1e3a5a', color: 'white', border: 'none', borderRadius: 6, padding: '9px', fontSize: 13, fontWeight: 600, cursor: form.surname ? 'pointer' : 'not-allowed' }}>
                    Далее →
                  </button>
                </div>
              </div>
            )}

            {/* Step 3: organization */}
            {step === 3 && (
              <div style={{ display: 'flex', flexDirection: 'column', gap: 14 }}>
                <div>
                  <Label>Организация</Label>
                  <Select value={form.organization_id} onChange={set('organization_id')} required>
                    <option value="">— Выберите организацию —</option>
                    {orgs.map(o => (
                      <option key={o.id} value={o.id}>{o.name}</option>
                    ))}
                  </Select>
                </div>
                <div>
                  <Label>Подразделение</Label>
                  <Select value={form.department_id} onChange={set('department_id')} required disabled={!form.organization_id}>
                    <option value="">— Выберите подразделение —</option>
                    {depts.map(d => (
                      <option key={d.id} value={d.id}>{d.name}</option>
                    ))}
                  </Select>
                </div>

                <ErrorMsg>{error}</ErrorMsg>

                <div style={{ display: 'flex', gap: 8, marginTop: 4 }}>
                  <button type="button" onClick={() => setStep(2)}
                    style={{ flex: 1, background: '#0b1526', color: '#94a3b8', border: '1px solid #1e3a5a', borderRadius: 6, padding: '8px', fontSize: 12, cursor: 'pointer' }}>
                    ← Назад
                  </button>
                  <BtnPrimary
                    type="submit"
                    loading={loading}
                    style={{ flex: 2, padding: '9px' }}
                  >
                    Зарегистрироваться
                  </BtnPrimary>
                </div>
              </div>
            )}
          </form>
        </div>

        <p style={{ textAlign: 'center', marginTop: 16 }}>
          <span style={{ color: '#64748b', fontSize: 12 }}>Уже есть аккаунт? </span>
          <Link to="/login" style={{ color: '#93c5fd', fontSize: 12, textDecoration: 'none', fontWeight: 500 }}>
            Войти
          </Link>
        </p>
      </div>
    </div>
  )
}
