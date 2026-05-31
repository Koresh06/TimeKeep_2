import { useState, useEffect } from 'react'

export function useFetch(fn, deps = []) {
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  const load = async () => {
    setLoading(true)
    setError(null)
    try {
      const res = await fn()
      setData(res.data)
    } catch (e) {
      setError(e.response?.data?.detail || 'Ошибка загрузки')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => { load() }, deps)

  return { data, loading, error, reload: load }
}
