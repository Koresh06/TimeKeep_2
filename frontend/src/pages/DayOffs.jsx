import { useState } from 'react'
import { useFetch } from '../hooks/useFetch'
import { getMyDayOffs, createDayOff, downloadReport } from '../api/dayoffs'
import Spinner from '../components/Spinner'

const STATUS_MAP = {
  pending: { label: 'Ожидает', cls: 'bg-yellow-900 text-yellow-300' },
  approved: { label: 'Одобрен', cls: 'bg-green-900 text-green-300' },
  rejected: { label: 'Отклонён', cls: 'bg-red-900 text-red-300' },
}

function StatusBadge({ status }) {
  const { label, cls } = STATUS_MAP[status] || { label: status, cls: 'bg-slate-700 text-slate-300' }
  return <span className={`text-xs px-2 py-0.5 rounded-full font-medium ${cls}`}>{label}</span>
}

export default function DayOffs() {
  const { data, loading, error, reload } = useFetch(getMyDayOffs)
  const [showForm, setShowForm] = useState(false)
  const [date, setDate] = useState('')
  const [submitting, setSubmitting] = useState(false)
  const [formError, setFormError] = useState('')
  const [downloading, setDownloading] = useState(null)

  const handleSubmit = async (e) => {
    e.preventDefault()
    setFormError('')
    setSubmitting(true)
    try {
      await createDayOff({ date })
      setDate('')
      setShowForm(false)
      reload()
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
    <div className="flex flex-col gap-6">
      <div className="flex justify-between items-center">
        <h2 className="text-2xl font-bold text-slate-100">Отгулы</h2>
        <button
          onClick={() => setShowForm(!showForm)}
          className="bg-blue-600 hover:bg-blue-500 text-white text-sm font-medium px-4 py-2 rounded-lg transition-colors"
        >
          {showForm ? 'Отмена' : '+ Взять отгул'}
        </button>
      </div>

      {showForm && (
        <form
          onSubmit={handleSubmit}
          className="bg-slate-900 border border-slate-700 rounded-xl p-5 flex flex-col gap-4"
        >
          <h3 className="text-slate-200 font-semibold">Новый отгул</h3>
          <div className="max-w-xs">
            <label className="block text-xs text-slate-400 mb-1">Дата</label>
            <input
              type="date"
              value={date}
              onChange={(e) => setDate(e.target.value)}
              required
              className="w-full bg-slate-800 border border-slate-600 rounded-lg px-3 py-2 text-sm text-slate-100 focus:outline-none focus:border-blue-500 transition-colors"
            />
          </div>
          {formError && <p className="text-red-400 text-xs">{formError}</p>}
          <button
            type="submit"
            disabled={submitting}
            className="self-start bg-blue-600 hover:bg-blue-500 disabled:opacity-50 text-white text-sm font-medium px-5 py-2 rounded-lg transition-colors"
          >
            {submitting ? 'Сохранение...' : 'Подать заявку'}
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
                  <th className="text-left px-4 py-3">Статус</th>
                  <th className="text-left px-4 py-3">Рапорт</th>
                </tr>
              </thead>
              <tbody>
                {data.map((d) => (
                  <tr key={d.id} className="border-b border-slate-800 hover:bg-slate-800/50 transition-colors">
                    <td className="px-4 py-3 text-slate-200">{d.date}</td>
                    <td className="px-4 py-3">
                      <StatusBadge status={d.status} />
                    </td>
                    <td className="px-4 py-3">
                      <button
                        onClick={() => handleDownload(d.id)}
                        disabled={downloading === d.id}
                        className="text-blue-400 hover:text-blue-300 text-xs disabled:opacity-50 transition-colors"
                      >
                        {downloading === d.id ? 'Загрузка...' : '↓ Скачать'}
                      </button>
                    </td>
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
