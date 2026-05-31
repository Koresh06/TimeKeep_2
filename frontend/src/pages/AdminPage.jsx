import { useState, useEffect, useCallback } from 'react'
import { useAuth, hasRole } from '../context/AuthContext'
import { getOrganizationUsers, updateUserWorkMode, activateUser, updateUserRole } from '../api/users'
import { getOrganizationDayOffs } from '../api/dayoffs'
import { getOrganizationOvertimes } from '../api/overtimes'
import Spinner from '../components/Spinner'
import {
  PageTitle, Card, SectionTitle, Select, Label,
  ErrorMsg, StatusBadge, TableContainer, Table, THead, Th, Td, TRow,
  EmptyState, Pagination,
} from '../components/ui'

function TabBtn({ active, onClick, children }) {
  return (
    <button
      onClick={onClick}
      style={{
        background: active ? 'rgba(200,30,30,0.12)' : 'transparent',
        border: 'none',
        borderBottom: active ? '2px solid #c81e1e' : '2px solid transparent',
        padding: '8px 18px',
        color: active ? '#f1f5f9' : '#4a6fa5',
        fontSize: 13, fontWeight: active ? 600 : 400,
        cursor: 'pointer', marginBottom: -1, transition: 'all 0.15s',
      }}
    >
      {children}
    </button>
  )
}

const ROLE_LABELS = { user: 'Сотрудник', moderator: 'Модератор', admin: 'Администратор', super_admin: 'Суперадмин' }
const MODE_LABELS = { daily: 'Ежедневный', shift: 'Сменный' }

export default function AdminPage() {
  const { tokenData } = useAuth()
  const isSuperAdmin = hasRole(tokenData, 'super_admin')

  const [tab, setTab] = useState('users')
  const [users, setUsers] = useState([])
  const [dayoffs, setDayoffs] = useState([])
  const [overtimes, setOvertimes] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [offset, setOffset] = useState(0)
  const [statusFilter, setStatusFilter] = useState('')
  const [actionState, setActionState] = useState({})
  const LIMIT = 15

  const load = useCallback(async () => {
    setLoading(true); setError(null)
    try {
      if (tab === 'users') {
        const r = await getOrganizationUsers({ offset, limit: LIMIT })
        setUsers(r.data || [])
      } else if (tab === 'dayoffs') {
        const params = { offset, limit: LIMIT }
        if (statusFilter) params.status = statusFilter
        const r = await getOrganizationDayOffs(params)
        setDayoffs(r.data || [])
      } else {
        const r = await getOrganizationOvertimes({ offset, limit: LIMIT })
        setOvertimes(r.data || [])
      }
    } catch (e) { setError(e.response?.data?.detail || 'Ошибка загрузки') }
    finally { setLoading(false) }
  }, [tab, offset, statusFilter])

  useEffect(() => { setOffset(0) }, [tab, statusFilter])
  useEffect(() => { load() }, [load])

  const handleWorkMode = async (userId, mode) => {
    setActionState(s => ({ ...s, [userId]: true }))
    try {
      await updateUserWorkMode(userId, mode)
      setUsers(list => list.map(u => u.id === userId ? { ...u, work_mode: mode } : u))
    } catch (e) { alert(e.response?.data?.detail || 'Ошибка') }
    finally { setActionState(s => ({ ...s, [userId]: false })) }
  }

  const handleActivate = async (userId, isActive) => {
    setActionState(s => ({ ...s, [`a${userId}`]: true }))
    try {
      await activateUser(userId, isActive)
      setUsers(list => list.map(u => u.id === userId ? { ...u, is_active: isActive } : u))
    } catch (e) { alert(e.response?.data?.detail || 'Ошибка') }
    finally { setActionState(s => ({ ...s, [`a${userId}`]: false })) }
  }

  const handleRole = async (userId, role) => {
    setActionState(s => ({ ...s, [`r${userId}`]: true }))
    try {
      await updateUserRole(userId, role)
      setUsers(list => list.map(u => u.id === userId ? { ...u, role } : u))
    } catch (e) { alert(e.response?.data?.detail || 'Ошибка') }
    finally { setActionState(s => ({ ...s, [`r${userId}`]: false })) }
  }

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 20 }}>
      <div>
        <PageTitle>Управление организацией</PageTitle>
        <p style={{ color: '#4a6fa5', fontSize: 12, margin: '4px 0 0' }}>
          Управление сотрудниками, переработками и отгулами
        </p>
      </div>

      {/* Tabs */}
      <div style={{ borderBottom: '1px solid #1e3a5a', display: 'flex', gap: 0 }}>
        <TabBtn active={tab === 'users'} onClick={() => setTab('users')}>Сотрудники</TabBtn>
        <TabBtn active={tab === 'dayoffs'} onClick={() => setTab('dayoffs')}>Отгулы</TabBtn>
        <TabBtn active={tab === 'overtimes'} onClick={() => setTab('overtimes')}>Переработки</TabBtn>
      </div>

      {/* Status filter for day-offs */}
      {tab === 'dayoffs' && (
        <div style={{ display: 'flex', gap: 8, alignItems: 'center', padding: '10px 14px', background: '#0f1e36', border: '1px solid #1e3a5a', borderRadius: 8, flexWrap: 'wrap' }}>
          <span style={{ color: '#4a6fa5', fontSize: 11, fontWeight: 600, textTransform: 'uppercase' }}>Статус:</span>
          {['', 'pending', 'approved', 'rejected'].map(s => (
            <button key={s} onClick={() => setStatusFilter(s)}
              style={{
                background: statusFilter === s ? 'rgba(200,30,30,0.15)' : 'transparent',
                border: `1px solid ${statusFilter === s ? '#c81e1e' : 'rgba(42,82,132,0.35)'}`,
                borderRadius: 5, padding: '3px 10px',
                color: statusFilter === s ? '#f87171' : '#94a3b8',
                fontSize: 11, cursor: 'pointer',
              }}>
              {s === '' ? 'Все' : s === 'pending' ? 'Ожидает' : s === 'approved' ? 'Одобрен' : 'Отклонён'}
            </button>
          ))}
        </div>
      )}

      {loading && <Spinner />}
      {error && <ErrorMsg>{error}</ErrorMsg>}

      {/* Users */}
      {!loading && tab === 'users' && (
        <TableContainer>
          {users.length === 0 ? <EmptyState message="Нет сотрудников" /> : (
            <>
              <Table>
                <THead>
                  <Th>ID</Th>
                  <Th>Логин</Th>
                  <Th>ФИО</Th>
                  <Th>Звание / Должность</Th>
                  <Th>Режим работы</Th>
                  <Th>Роль</Th>
                  <Th>Статус</Th>
                  <Th>Действия</Th>
                </THead>
                <tbody>
                  {users.map(u => (
                    <TRow key={u.id}>
                      <Td style={{ color: '#4a6fa5', fontSize: 12 }}>{u.id}</Td>
                      <Td style={{ color: '#93c5fd' }}>{u.login}</Td>
                      <Td style={{ color: '#e2e8f0', fontWeight: 500 }}>
                        {[u.surname, u.first_name, u.patronymic].filter(Boolean).join(' ')}
                      </Td>
                      <Td style={{ color: '#94a3b8', fontSize: 12 }}>
                        <div>{u.rank}</div>
                        <div style={{ color: '#4a6fa5', marginTop: 2 }}>{u.position}</div>
                      </Td>
                      <Td>
                        <select
                          value={u.work_mode}
                          disabled={actionState[u.id]}
                          onChange={e => handleWorkMode(u.id, e.target.value)}
                          style={{
                            background: '#0b1526', border: '1px solid #1e3a5a',
                            borderRadius: 4, padding: '3px 6px', color: '#fbbf24',
                            fontSize: 11, cursor: 'pointer',
                          }}
                        >
                          <option value="daily">Ежедневный</option>
                          <option value="shift">Сменный</option>
                        </select>
                      </Td>
                      <Td>
                        {isSuperAdmin ? (
                          <select
                            value={u.role}
                            disabled={actionState[`r${u.id}`]}
                            onChange={e => handleRole(u.id, e.target.value)}
                            style={{
                              background: '#0b1526', border: '1px solid #1e3a5a',
                              borderRadius: 4, padding: '3px 6px', color: '#93c5fd',
                              fontSize: 11, cursor: 'pointer',
                            }}
                          >
                            {Object.entries(ROLE_LABELS).map(([v, l]) => (
                              <option key={v} value={v}>{l}</option>
                            ))}
                          </select>
                        ) : (
                          <span style={{ color: '#93c5fd', fontSize: 12 }}>
                            {ROLE_LABELS[u.role] || u.role}
                          </span>
                        )}
                      </Td>
                      <Td>
                        <span style={{ color: u.is_active ? '#4ade80' : '#f87171', fontSize: 12 }}>
                          {u.is_active ? '● Активен' : '○ Неактивен'}
                        </span>
                      </Td>
                      <Td>
                        {isSuperAdmin && (
                          <button
                            onClick={() => handleActivate(u.id, !u.is_active)}
                            disabled={actionState[`a${u.id}`]}
                            style={{
                              background: u.is_active ? 'rgba(200,30,30,0.1)' : 'rgba(34,197,94,0.1)',
                              color: u.is_active ? '#f87171' : '#4ade80',
                              border: `1px solid ${u.is_active ? 'rgba(200,30,30,0.3)' : 'rgba(34,197,94,0.3)'}`,
                              borderRadius: 4, padding: '3px 8px', fontSize: 11, cursor: 'pointer',
                            }}
                          >
                            {u.is_active ? 'Деактивировать' : 'Активировать'}
                          </button>
                        )}
                      </Td>
                    </TRow>
                  ))}
                </tbody>
              </Table>
              <Pagination offset={offset} limit={LIMIT} onChangePage={setOffset} />
            </>
          )}
        </TableContainer>
      )}

      {/* Day-offs */}
      {!loading && tab === 'dayoffs' && (
        <TableContainer>
          {dayoffs.length === 0 ? <EmptyState /> : (
            <>
              <Table>
                <THead>
                  <Th>ID</Th>
                  <Th>Сотрудник</Th>
                  <Th>Дата</Th>
                  <Th>Статус</Th>
                  <Th>Переработок</Th>
                  <Th>Создана</Th>
                </THead>
                <tbody>
                  {dayoffs.map(d => (
                    <TRow key={d.id}>
                      <Td style={{ color: '#4a6fa5', fontSize: 12 }}>{d.id}</Td>
                      <Td style={{ color: '#93c5fd' }}>{d.user_id}</Td>
                      <Td style={{ fontWeight: 500, color: '#f1f5f9' }}>{d.date_}</Td>
                      <Td><StatusBadge status={d.status} /></Td>
                      <Td style={{ color: '#94a3b8' }}>{d.overtimes?.length || 0}</Td>
                      <Td style={{ color: '#4a6fa5', fontSize: 12 }}>{d.created_at?.slice(0, 10)}</Td>
                    </TRow>
                  ))}
                </tbody>
              </Table>
              <Pagination offset={offset} limit={LIMIT} onChangePage={setOffset} />
            </>
          )}
        </TableContainer>
      )}

      {/* Overtimes */}
      {!loading && tab === 'overtimes' && (
        <TableContainer>
          {overtimes.length === 0 ? <EmptyState /> : (
            <>
              <Table>
                <THead>
                  <Th>Сотрудник</Th>
                  <Th>Дата</Th>
                  <Th>Начало</Th>
                  <Th>Конец</Th>
                  <Th>Часов</Th>
                  <Th>Статус</Th>
                </THead>
                <tbody>
                  {overtimes.map(o => {
                    const [fh, fm] = (o.start_time || '0:0').split(':').map(Number)
                    const [th, tm] = (o.end_time || '0:0').split(':').map(Number)
                    const dur = ((th * 60 + tm) - (fh * 60 + fm)) / 60
                    return (
                      <TRow key={o.id}>
                        <Td style={{ color: '#93c5fd' }}>{o.user_id}</Td>
                        <Td style={{ fontWeight: 500, color: '#f1f5f9' }}>{o.date_}</Td>
                        <Td style={{ color: '#94a3b8' }}>{o.start_time?.slice(0, 5)}</Td>
                        <Td style={{ color: '#94a3b8' }}>{o.end_time?.slice(0, 5)}</Td>
                        <Td style={{ color: '#4ade80', fontWeight: 600 }}>{dur > 0 ? `${dur.toFixed(1)} ч` : '—'}</Td>
                        <Td><StatusBadge status={o.status} /></Td>
                      </TRow>
                    )
                  })}
                </tbody>
              </Table>
              <Pagination offset={offset} limit={LIMIT} onChangePage={setOffset} />
            </>
          )}
        </TableContainer>
      )}
    </div>
  )
}
