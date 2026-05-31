import { useState } from 'react'
import { useFetch } from '../hooks/useFetch'
import { getMyOvertimes, createOvertime } from '../api/overtimes'
import Spinner from '../components/Spinner'

const empty = { date: '', time_from: '', time_to: '', description: '' }

export default function Overtimes() {
  const { data, loading, error, reload } = useFetch(getMyOvertimes)
  const [form, setForm] = useState(empty)
  const [submitting, setSubmitting] = useState(false)
  const [formError, setFormError] = useState('')
  const [showForm, setShowForm] = useState(false)

  const handleSubmit = async (e) => {
    e.preventDefault()
    setFormError('')
    setSubmitting(true)
    try {
      await createOvertime(form)
      setForm(empty)
      setShowForm(false)
      reload()
    } catch (e) {
      setFormError(e.response?.data?.detail || 'Ошибка при сохранении')
    } finally {
      setSubmitting(false)
    }
  }

  const field = (key, label, type = 'text') => (
    <div>
      <label className="block text-xs text-slate-400 mb-1">{label}</label>
      <input
        type={type}
        value={form[key]}
        onChange={(e) => setForm({ ...form, [key]: e.target.value })}
        required={key !== 'description'}
        className="w-full bg-slate-800 border border-slate-600 rounded-lg px-3 py-2 text-sm text-slate-100 focus:outline-none focus:border-blue-500 transition-colors"
      />
    </div>
  )

  return (
    <div className="flex flex-col gap-6">
      <div className="flex justify-between items-center">
        <h2 className="text-2xl font-bold text-slate-100">Переработки</h2>
        <button
          onClick={() => setShowForm(!showForm)}
          className="bg-blue-600 hover:bg-blue-500 text-white text-sm font-medium px-4 py-2 rounded-lg transition-colors"
        >
          {showForm ? 'Отмена' : '+ Добавить'}
        </button>
      </div>

      {showForm && (
        <form
          onSubmit={handleSubmit}
          className="bg-slate-900 border border-slate-700 rounded-xl p-5 flex flex-col gap-4"
        >
          <h3 className="text-slate-200 font-semibold">Новая переработка</h3>
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
            {field('date', 'Дата', 'date')}
            {field('time_from', 'Начало', 'time')}
            {field('time_to', 'Конец', 'time')}
          </div>
          {field('description', 'Описание (необязательно)')}
          {formError && <p className="text-red-400 text-xs">{formError}</p>}
          <button
            type="submit"
            disabled={submitting}
            className="self-start bg-blue-600 hover:bg-blue-500 disabled:opacity-50 text-white text-sm font-medium px-5 py-2 rounded-lg transition-colors"
          >
            {submitting ? 'Сохранение...' : 'Сохранить'}
          </button>
        </form>
      )}

      {loading && <Spinner />}
      {error && <p className="text-red-400 text-sm">{error}</p>}
      {!loading && !error && (
        <div className="bg-slate-900 border border-slate-700 rounded-xl overflow-hidden">
          {!data || data.length === 0 ? (
            <p className="p-5 text-slate-500 text-sm">Нет записей</p>
          ) : (
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-slate-700 text-slate-400 text-xs uppercase">
                  <th className="text-left px-4 py-3">Дата</th>
                  <th className="text-left px-4 py-3">Начало</th>
                  <th className="text-left px-4 py-3">Конец</th>
                  <th className="text-left px-4 py-3">Описание</th>
                </tr>
              </thead>
              <tbody>
                {data.map((o) => (
                  <tr key={o.id} className="border-b border-slate-800 hover:bg-slate-800/50 transition-colors">
                    <td className="px-4 py-3 text-slate-200">{o.date}</td>
                    <td className="px-4 py-3 text-slate-300">{o.time_from}</td>
                    <td className="px-4 py-3 text-slate-300">{o.time_to}</td>
                    <td className="px-4 py-3 text-slate-400">{o.description || '—'}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>
      )}
    </div>
  )
}
