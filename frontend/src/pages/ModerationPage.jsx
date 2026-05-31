import { useState, useEffect, useCallback } from 'react'
import { getDepartmentDayOffs, moderateDayOff } from '../api/dayoffs'
import { getDepartmentOvertimes } from '../api/overtimes'
import { getDepartmentUsers } from '../api/users'
import Spinner from '../components/Spinner'
import {
  PageTitle, Card, SectionTitle, Select, Label, BtnPrimary, BtnSecondary,
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
        fontSize: 13,
        fontWeight: active ? 600 : 400,
        cursor: 'pointer',
        marginBottom: -1,
        transition: 'all 0.15s',
      }}
    >
      {children}
    </button>
  )
}

export default function ModerationPage() {
  const [tab, setTab] = useState('dayoffs')
  const [dayoffs, setDayoffs] = useState([])
  const [overtimes, setOvertimes] = useState([])
  const [users, setUsers] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [statusFilter, setStatusFilter] = useState('')
  const [offset, setOffset] = useState(0)
  const [moderating, setModerating] = useState(null)
  const LIMIT = 15

  const loadDayoffs = useCallback(async () => {
    setLoading(true); setError(null)
    try {
      const params = { offset, limit: LIMIT }
      if (statusFilter) params.status = statusFilter
      const res = await getDepartmentDayOffs(params)
      setDayoffs(res.data || [])
    } catch (e) { setError(e.response?.data?.detail || 'Ошибка загрузки') }
    finally { setLoading(false) }
  }, [offset, statusFilter])

  const loadOvertimes = useCallback(async () => {
    setLoading(true); setError(null)
    try {
      const res = await getDepartmentOvertimes({ offset, limit: LIMIT })
      setOvertimes(res.data || [])
    } catch (e) { setError(e.response?.data?.detail || 'Ошибка загрузки') }
    finally { setLoading(false) }
  }, [offset])

  const loadUsers = useCallback(async () => {
    setLoading(true); setError(null)
    try {
      const res = await getDepartmentUsers({ offset, limit: LIMIT })
      setUsers(res.data || [])
    } catch (e) { setError(e.response?.data?.detail || 'Ошибка загрузки') }
    finally { setLoading(false) }
  }, [offset])

  useEffect(() => {
    setOffset(0)
  }, [tab, statusFilter])

  useEffect(() => {
    if (tab === 'dayoffs') loadDayoffs()
    else if (tab === 'overtimes') loadOvertimes()
    else if (tab === 'users') loadUsers()
  }, [tab, offset, loadDayoffs, loadOvertimes, loadUsers])

  const handleModerate = async (id, isApproved) => {
    setModerating(id)
    try {
      await moderateDayOff(id, isApproved)
      setDayoffs(list => list.map(d =>
        d.id === id ? { ...d, status: isApproved ? 'approved' : 'rejected' } : d
      ))
    } catch (e) {
      alert(e.response?.data?.detail || 'Ошибка при модерации')
    } finally {
      setModerating(null)
    }
  }

  const ROLE_LABELS = { user: 'Сотрудник', moderator: 'Модератор', admin: 'Администратор', super_admin: 'Суперадмин' }
  const MODE_LABELS = { daily: 'Ежедневный', shift: 'Сменный' }

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 20 }}>
      <div>
        <PageTitle>Управление отделом</PageTitle>
        <p style={{ color: '#4a6fa5', fontSize: 12, margin: '4px 0 0' }}>
          Просмотр и модерация данных подразделения
        </p>
      </div>

      {/* Tabs */}
      <div style={{ borderBottom: '1px solid #1e3a5a', display: 'flex', gap: 0 }}>
        <TabBtn active={tab === 'dayoffs'} onClick={() => setTab('dayoffs')}>
          Отгулы
        </TabBtn>
        <TabBtn active={tab === 'overtimes'} onClick={() => setTab('overtimes')}>
          Переработки
        </TabBtn>
        <TabBtn active={tab === 'users'} onClick={() => setTab('users')}>
          Сотрудники
        </TabBtn>
      </div>

      {/* Filters for day-offs tab */}
      {tab === 'dayoffs' && (
        <div
          style={{
            display: 'flex', gap: 8, alignItems: 'center', flexWrap: 'wrap',
            padding: '10px 14px', background: '#0f1e36', border: '1px solid #1e3a5a', borderRadius: 8,
          }}
        >
          <span style={{ color: '#4a6fa5', fontSize: 11, fontWeight: 600, textTransform: 'uppercase', letterSpacing: '0.5px' }}>
            Статус:
          </span>
          {['', 'pending', 'approved', 'rejected'].map(s => (
            <button key={s} onClick={() => setStatusFilter(s)}
              style={{
                background: statusFilter === s ? 'rgba(200,30,30,0.15)' : 'transparent',
                border: `1px solid ${statusFilter === s ? '#c81e1e' : 'rgba(42,82,132,0.35)'}`,
                borderRadius: 5, padding: '3px 10px',
                color: statusFilter === s ? '#f87171' : '#94a3b8',
                fontSize: 11, cursor: 'pointer', fontWeight: statusFilter === s ? 600 : 400,
              }}
            >
              {s === '' ? 'Все' : s === 'pending' ? 'Ожидает' : s === 'approved' ? 'Одобрен' : 'Отклонён'}
            </button>
          ))}
        </div>
      )}

      {loading && <Spinner />}
      {error && <ErrorMsg>{error}</ErrorMsg>}

      {/* Day-offs table */}
      {!loading && tab === 'dayoffs' && (
        <TableContainer>
          {dayoffs.length === 0 ? <EmptyState /> : (
            <>
              <Table>
                <THead>
                  <Th>ID</Th>
                  <Th>Сотрудник ID</Th>
                  <Th>Дата</Th>
                  <Th>Статус</Th>
                  <Th>Создана</Th>
                  <Th>Действие</Th>
                </THead>
                <tbody>
                  {dayoffs.map(d => (
                    <TRow key={d.id}>
                      <Td style={{ color: '#4a6fa5', fontSize: 12 }}>{d.id}</Td>
                      <Td style={{ color: '#93c5fd' }}>{d.user_id}</Td>
                      <Td style={{ fontWeight: 500, color: '#f1f5f9' }}>{d.date_}</Td>
                      <Td><StatusBadge status={d.status} /></Td>
                      <Td style={{ color: '#4a6fa5', fontSize: 12 }}>{d.created_at?.slice(0, 10)}</Td>
                      <Td>
                        {d.status === 'pending' && (
                          <div style={{ display: 'flex', gap: 6 }}>
                            <button
                              onClick={() => handleModerate(d.id, true)}
                              disabled={moderating === d.id}
                              style={{
                                background: 'rgba(34,197,94,0.12)', color: '#4ade80',
                                border: '1px solid rgba(34,197,94,0.3)', borderRadius: 5,
                                padding: '3px 10px', fontSize: 11, cursor: 'pointer', fontWeight: 600,
                              }}
                            >
                              ✓ Одобрить
                            </button>
                            <button
                              onClick={() => handleModerate(d.id, false)}
                              disabled={moderating === d.id}
                              style={{
                                background: 'rgba(200,30,30,0.1)', color: '#f87171',
                                border: '1px solid rgba(200,30,30,0.25)', borderRadius: 5,
                                padding: '3px 10px', fontSize: 11, cursor: 'pointer', fontWeight: 600,
                              }}
                            >
                              ✗ Отклонить
                            </button>
                          </div>
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

      {/* Overtimes table */}
      {!loading && tab === 'overtimes' && (
        <TableContainer>
          {overtimes.length === 0 ? <EmptyState /> : (
            <>
              <Table>
                <THead>
                  <Th>Сотрудник ID</Th>
                  <Th>Дата</Th>
                  <Th>Начало</Th>
                  <Th>Конец</Th>
                  <Th>Часов</Th>
                  <Th>Статус</Th>
                  <Th>Описание</Th>
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
                        <Td style={{ color: '#4a6fa5', fontSize: 12, maxWidth: 160 }}>{o.description || '—'}</Td>
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

      {/* Users table */}
      {!loading && tab === 'users' && (
        <TableContainer>
          {users.length === 0 ? <EmptyState message="Нет сотрудников" /> : (
            <>
              <Table>
                <THead>
                  <Th>ID</Th>
                  <Th>Логин</Th>
                  <Th>ФИО</Th>
                  <Th>Звание</Th>
                  <Th>Режим</Th>
                  <Th>Роль</Th>
                  <Th>Статус</Th>
                </THead>
                <tbody>
                  {users.map(u => (
                    <TRow key={u.id}>
                      <Td style={{ color: '#4a6fa5', fontSize: 12 }}>{u.id}</Td>
                      <Td style={{ color: '#93c5fd' }}>{u.login}</Td>
                      <Td style={{ color: '#e2e8f0', fontWeight: 500 }}>
                        {[u.surname, u.first_name, u.patronymic].filter(Boolean).join(' ')}
                      </Td>
                      <Td style={{ color: '#94a3b8', fontSize: 12 }}>{u.rank}</Td>
                      <Td><span style={{ color: '#fbbf24', fontSize: 12 }}>{MODE_LABELS[u.work_mode] || u.work_mode}</span></Td>
                      <Td><span style={{ color: '#93c5fd', fontSize: 12 }}>{ROLE_LABELS[u.role] || u.role}</span></Td>
                      <Td>
                        <span style={{ color: u.is_active ? '#4ade80' : '#f87171', fontSize: 12 }}>
                          {u.is_active ? '● Активен' : '○ Неактивен'}
                        </span>
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
    </div>
  )
}
