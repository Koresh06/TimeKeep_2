import { useState, useEffect, useCallback } from 'react'
import { getMyOvertimes, createOvertime, deleteOvertime } from '../api/overtimes'
import Spinner from '../components/Spinner'
import {
  PageTitle, Card, SectionTitle, Label, Input, BtnPrimary, BtnDanger, BtnSecondary,
  ErrorMsg, StatusBadge, TableContainer, Table, THead, Th, Td, TRow, EmptyState,
  Pagination,
} from '../components/ui'

const empty = { date: '', start_time: '', end_time: '', description: '' }

export default function Overtimes() {
  const [data, setData] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [form, setForm] = useState(empty)
  const [submitting, setSubmitting] = useState(false)
  const [formError, setFormError] = useState('')
  const [showForm, setShowForm] = useState(false)
  const [offset, setOffset] = useState(0)
  const [deletingId, setDeletingId] = useState(null)
  const LIMIT = 15

  const load = useCallback(async () => {
    setLoading(true)
    setError(null)
    try {
      const res = await getMyOvertimes({ offset, limit: LIMIT })
      setData(res.data || [])
    } catch (e) {
      setError(e.response?.data?.detail || 'Ошибка загрузки')
    } finally {
      setLoading(false)
    }
  }, [offset])

  useEffect(() => { load() }, [load])

  const handleSubmit = async (e) => {
    e.preventDefault()
    setFormError('')
    setSubmitting(true)
    try {
      await createOvertime(form)
      setForm(empty)
      setShowForm(false)
      setOffset(0)
      load()
    } catch (e) {
      setFormError(e.response?.data?.detail || 'Ошибка при сохранении')
    } finally {
      setSubmitting(false)
    }
  }

  const handleDelete = async (id) => {
    if (!confirm('Удалить переработку?')) return
    setDeletingId(id)
    try {
      await deleteOvertime(id)
      setData(d => d.filter(o => o.id !== id))
    } catch (e) {
      alert(e.response?.data?.detail || 'Ошибка при удалении')
    } finally {
      setDeletingId(null)
    }
  }

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 20 }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: 10 }}>
        <PageTitle>Мои переработки</PageTitle>
        <BtnPrimary onClick={() => setShowForm(!showForm)}>
          {showForm ? 'Отмена' : '+ Добавить'}
        </BtnPrimary>
      </div>

      {showForm && (
        <Card style={{ padding: 20 }}>
          <SectionTitle style={{ marginBottom: 16 }}>Новая переработка</SectionTitle>
          <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: 14 }}>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(160px, 1fr))', gap: 12 }}>
              <div>
                <Label>Дата</Label>
                <Input type="date" value={form.date}
                  onChange={e => setForm({ ...form, date: e.target.value })} required />
              </div>
              <div>
                <Label>Начало</Label>
                <Input type="time" value={form.start_time}
                  onChange={e => setForm({ ...form, start_time: e.target.value })} required />
              </div>
              <div>
                <Label>Конец</Label>
                <Input type="time" value={form.end_time}
                  onChange={e => setForm({ ...form, end_time: e.target.value })} required />
              </div>
            </div>
            <div>
              <Label>Описание (необязательно)</Label>
              <Input value={form.description}
                onChange={e => setForm({ ...form, description: e.target.value })}
                placeholder="Причина переработки" />
            </div>
            <ErrorMsg>{formError}</ErrorMsg>
            <BtnPrimary type="submit" loading={submitting} style={{ alignSelf: 'flex-start' }}>
              Сохранить переработку
            </BtnPrimary>
          </form>
        </Card>
      )}

      {loading && <Spinner />}
      {error && <ErrorMsg>{error}</ErrorMsg>}

      {!loading && !error && (
        <TableContainer>
          {data.length === 0 ? (
            <EmptyState message={offset > 0 ? 'Больше записей нет' : 'Нет переработок'} />
          ) : (
            <>
              <Table>
                <THead>
                  <Th>Дата</Th>
                  <Th>Начало</Th>
                  <Th>Конец</Th>
                  <Th>Часов</Th>
                  <Th>Описание</Th>
                  <Th>Статус</Th>
                  <Th></Th>
                </THead>
                <tbody>
                  {data.map(o => {
                    const [fh, fm] = (o.start_time || '0:0').split(':').map(Number)
                    const [th, tm] = (o.end_time || '0:0').split(':').map(Number)
                    const dur = ((th * 60 + tm) - (fh * 60 + fm)) / 60
                    return (
                      <TRow key={o.id}>
                        <Td style={{ fontWeight: 500, color: '#f1f5f9' }}>{o.date_}</Td>
                        <Td style={{ color: '#93c5fd' }}>{o.start_time?.slice(0, 5)}</Td>
                        <Td style={{ color: '#93c5fd' }}>{o.end_time?.slice(0, 5)}</Td>
                        <Td style={{ color: '#4ade80', fontWeight: 600 }}>
                          {dur > 0 ? `${dur.toFixed(1)} ч` : '—'}
                        </Td>
                        <Td style={{ color: '#94a3b8', maxWidth: 200 }}>
                          {o.description || '—'}
                        </Td>
                        <Td><StatusBadge status={o.status} /></Td>
                        <Td>
                          {o.status === 'active' && (
                            <BtnDanger
                              onClick={() => handleDelete(o.id)}
                              disabled={deletingId === o.id}
                            >
                              {deletingId === o.id ? '...' : 'Удалить'}
                            </BtnDanger>
                          )}
                        </Td>
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
