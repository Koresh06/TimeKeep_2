import { useFetch } from '../hooks/useFetch'
import { getMyOvertimes } from '../api/overtimes'
import { getMyDayOffs } from '../api/dayoffs'
import Spinner from '../components/Spinner'
import { Link } from 'react-router-dom'

function totalMinutes(overtimes) {
  return (overtimes || []).reduce((acc, o) => {
    const [fh, fm] = o.time_from.split(':').map(Number)
    const [th, tm] = o.time_to.split(':').map(Number)
    return acc + (th * 60 + tm) - (fh * 60 + fm)
  }, 0)
}

function formatHours(minutes) {
  const h = Math.floor(minutes / 60)
  const m = minutes % 60
  return m > 0 ? `${h} ч ${m} мин` : `${h} ч`
}

function StatusBadge({ status }) {
  const map = {
    pending: { label: 'Ожидает', cls: 'bg-yellow-900 text-yellow-300' },
    approved: { label: 'Одобрен', cls: 'bg-green-900 text-green-300' },
    rejected: { label: 'Отклонён', cls: 'bg-red-900 text-red-300' },
  }
  const { label, cls } = map[status] || { label: status, cls: 'bg-slate-700 text-slate-300' }
  return <span className={`text-xs px-2 py-0.5 rounded-full font-medium ${cls}`}>{label}</span>
}

export default function Dashboard() {
  const { data: overtimes, loading: lo } = useFetch(getMyOvertimes)
  const { data: dayoffs, loading: ld } = useFetch(getMyDayOffs)

  if (lo || ld) return <Spinner />

  const mins = totalMinutes(overtimes)
  const recent = (dayoffs || []).slice(0, 5)

  return (
    <div className="flex flex-col gap-6">
      <h2 className="text-2xl font-bold text-slate-100">Главная</h2>

      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <StatCard label="Переработок" value={(overtimes || []).length} />
        <StatCard label="Всего часов" value={formatHours(mins)} />
        <StatCard label="Отгулов" value={(dayoffs || []).length} />
      </div>

      <div className="bg-slate-900 border border-slate-700 rounded-xl p-5">
        <div className="flex justify-between items-center mb-4">
          <h3 className="text-slate-200 font-semibold">Последние отгулы</h3>
          <Link to="/day-offs" className="text-blue-400 text-sm hover:underline">Все →</Link>
        </div>
        {recent.length === 0 ? (
          <p className="text-slate-500 text-sm">Нет отгулов</p>
        ) : (
          <ul className="flex flex-col gap-3">
            {recent.map((d) => (
              <li key={d.id} className="flex justify-between items-center text-sm">
                <span className="text-slate-300">{d.date}</span>
                <StatusBadge status={d.status} />
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  )
}

function StatCard({ label, value }) {
  return (
    <div className="bg-slate-900 border border-slate-700 rounded-xl p-5">
      <p className="text-slate-400 text-xs mb-1">{label}</p>
      <p className="text-2xl font-bold text-slate-100">{value}</p>
    </div>
  )
}
