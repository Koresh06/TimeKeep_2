import { useState, useEffect, useCallback } from 'react'
import { getMyDayOffs, createDayOff, downloadReport } from '../api/dayoffs'
import Spinner from '../components/Spinner'
import {
  PageTitle, Card, SectionTitle, Label, Input, Select, BtnPrimary, BtnSecondary,
  ErrorMsg, StatusBadge, TableContainer, Table, THead, Th, Td, TRow, EmptyState,
  Pagination,
} from '../components/ui'

export default function DayOffs() {
  const [data, setData] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [showForm, setShowForm] = useState(false)
  const [date, setDate] = useState('')
  const [submitting, setSubmitting] = useState(false)
  const [formError, setFormError] = useState('')
  const [downloading, setDownloading] = useState(null)
  const [offset, setOffset] = useState(0)
  const [statusFilter, setStatusFilter] = useState('')
  const LIMIT = 15

  const load = useCallback(async () => {
    setLoading(true)
    setError(null)
    try {
      const params = { offset, limit: LIMIT }
      if (statusFilter) params.status = statusFilter
      const res = await getMyDayOffs(params)
      setData(res.data || [])
    } catch (e) {
      setError(e.response?.data?.detail || 'Ошибка загрузки')
    } finally {
      setLoading(false)
    }
  }, [offset, statusFilter])

  useEffect(() => { load() }, [load])

  const handleSubmit = async (e) => {
    e.preventDefault()
    setFormError('')
    setSubmitting(true)
    try {
      await createDayOff({ date })
      setDate('')
      setShowForm(false)
      setOffset(0)
      load()
    } catch (e) {
      setFormError(e.response?.data?.detail || 'Ошибка при сохранении')
    } finally {
      setSubmitting(false)
    }
  }

  const handleDownload = async (id) => {
    setDownloading(id)
    try {
      await downloadReport(id)
    } catch {
      alert('Ошибка при скачивании рапорта')
    } finally {
      setDownloading(null)
    }
  }

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 20 }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: 10 }}>
        <PageTitle>Мои отгулы</PageTitle>
        <BtnPrimary onClick={() => setShowForm(!showForm)}>
          {showForm ? 'Отмена' : '+ Оформить отгул'}
        </BtnPrimary>
      </div>

      {showForm && (
        <Card style={{ padding: 20 }}>
          <SectionTitle style={{ marginBottom: 16 }}>Заявка на отгул</SectionTitle>
          <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: 14, maxWidth: 320 }}>
            <div>
              <Label>Дата отгула</Label>
              <Input
                type="date"
                value={date}
                onChange={e => setDate(e.target.value)}
                required
              />
            </div>
            <div
              style={{
                background: 'rgba(26,75,140,0.1)',
                border: '1px solid rgba(26,75,140,0.3)',
                borderRadius: 6,
                padding: '10px 12px',
                fontSize: 12,
                color: '#93c5fd',
              }}
            >
              💡 Система автоматически спишет накопленные часы для выбранной даты
            </div>
            <ErrorMsg>{formError}</ErrorMsg>
            <BtnPrimary type="submit" loading={submitting} style={{ alignSelf: 'flex-start' }}>
              Подать заявку
            </BtnPrimary>
          </form>
        </Card>
      )}

      {/* Filters */}
      <div
        style={{
          display: 'flex',
          gap: 10,
          alignItems: 'center',
          padding: '12px 16px',
          background: '#0f1e36',
          border: '1px solid #1e3a5a',
          borderRadius: 8,
          flexWrap: 'wrap',
        }}
      >
        <span style={{ color: '#4a6fa5', fontSize: 12, fontWeight: 600, textTransform: 'uppercase', letterSpacing: '0.5px' }}>
          Фильтр:
        </span>
        {['', 'pending', 'approved', 'rejected'].map(s => (
          <button
            key={s}
            onClick={() => { setStatusFilter(s); setOffset(0) }}
            style={{
              background: statusFilter === s ? 'rgba(200,30,30,0.15)' : 'transparent',
              border: `1px solid ${statusFilter === s ? '#c81e1e' : 'rgba(42,82,132,0.35)'}`,
              borderRadius: 5,
              padding: '4px 12px',
              color: statusFilter === s ? '#f87171' : '#94a3b8',
              fontSize: 12,
              cursor: 'pointer',
              fontWeight: statusFilter === s ? 600 : 400,
            }}
          >
            {s === '' ? 'Все' : s === 'pending' ? 'Ожидает' : s === 'approved' ? 'Одобрен' : 'Отклонён'}
          </button>
        ))}
      </div>

      {loading && <Spinner />}
      {error && <ErrorMsg>{error}</ErrorMsg>}

      {!loading && !error && (
        <TableContainer>
          {data.length === 0 ? (
            <EmptyState message={offset > 0 ? 'Больше записей нет' : 'Нет отгулов'} />
          ) : (
            <>
              <Table>
                <THead>
                  <Th>Дата</Th>
                  <Th>Статус</Th>
                  <Th>Переработок</Th>
                  <Th>Создана</Th>
                  <Th>Рапорт</Th>
                </THead>
                <tbody>
                  {data.map(d => (
                    <TRow key={d.id}>
                      <Td style={{ fontWeight: 500, color: '#f1f5f9' }}>{d.date_}</Td>
                      <Td><StatusBadge status={d.status} /></Td>
                      <Td style={{ color: '#94a3b8' }}>{d.overtimes?.length || 0}</Td>
                      <Td style={{ color: '#4a6fa5', fontSize: 12 }}>
                        {d.created_at?.slice(0, 10)}
                      </Td>
                      <Td>
                        {d.status === 'approved' && (
                          <button
                            onClick={() => handleDownload(d.id)}
                            disabled={downloading === d.id}
                            style={{
                              background: 'rgba(34,197,94,0.1)',
                              color: downloading === d.id ? '#4a6fa5' : '#4ade80',
                              border: '1px solid rgba(34,197,94,0.25)',
                              borderRadius: 5,
                              padding: '4px 10px',
                              fontSize: 11,
                              cursor: downloading === d.id ? 'not-allowed' : 'pointer',
                              fontWeight: 500,
                            }}
                          >
                            {downloading === d.id ? 'Загрузка...' : '↓ Скачать рапорт'}
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
    </div>
  )
}
