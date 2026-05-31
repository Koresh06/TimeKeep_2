import api from './axios'

export const getMyDayOffs = () => api.get('/day-offs/me')
export const createDayOff = (data) => api.post('/day-offs', data)
export const downloadReport = async (id) => {
  const res = await api.get(`/day-offs/${id}/report`, { responseType: 'blob' })
  const url = URL.createObjectURL(res.data)
  const a = document.createElement('a')
  a.href = url
  a.download = `report-${id}.pdf`
  a.click()
  URL.revokeObjectURL(url)
}
