import { useFetch } from '../hooks/useFetch'
import { getMe } from '../api/users'
import Spinner from '../components/Spinner'

function Row({ label, value }) {
  return (
    <div className="flex justify-between items-center py-3 border-b border-slate-800 last:border-0">
      <span className="text-slate-400 text-sm">{label}</span>
      <span className="text-slate-100 text-sm font-medium">{value || '—'}</span>
    </div>
  )
}

export default function Profile() {
  const { data: user, loading, error } = useFetch(getMe)

  if (loading) return <Spinner />
  if (error) return <p className="text-red-400 text-sm">{error}</p>

  return (
    <div className="flex flex-col gap-6">
      <h2 className="text-2xl font-bold text-slate-100">Профиль</h2>
      <div className="bg-slate-900 border border-slate-700 rounded-xl p-5">
        <div className="flex items-center gap-4 mb-6 pb-5 border-b border-slate-700">
          <div className="w-14 h-14 rounded-full bg-blue-600 flex items-center justify-center text-white text-xl font-bold select-none">
            {user?.full_name?.[0]?.toUpperCase() || user?.username?.[0]?.toUpperCase() || '?'}
          </div>
          <div>
            <p className="text-slate-100 font-semibold text-lg">{user?.full_name || user?.username}</p>
            <p className="text-slate-400 text-sm">@{user?.username}</p>
          </div>
        </div>
        <Row label="Email" value={user?.email} />
        <Row label="Должность" value={user?.rank} />
        <Row label="Отдел" value={user?.department?.name} />
        <Row label="Организация" value={user?.organization?.name} />
        <Row label="Роль" value={user?.role} />
      </div>
    </div>
  )
}
