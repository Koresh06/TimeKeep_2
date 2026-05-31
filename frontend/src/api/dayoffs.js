import api from './axios'

export const getMyDayOffs = (params = {}) =>
  api.get('/day-offs/me', { params })

export const getDepartmentDayOffs = (params = {}) =>
  api.get('/day-offs/current-department', { params })

export const getOrganizationDayOffs = (params = {}) =>
  api.get('/day-offs/current-organization', { params })

export const getAllDayOffs = (params = {}) =>
  api.get('/day-offs', { params })

export const createDayOff = (data) =>
  api.post('/day-offs', { date_: data.date })

export const moderateDayOff = (id, is_approved) =>
  api.patch(`/day-offs/${id}/moderate`, null, { params: { is_approved } })

export const downloadReport = async (id) => {
  const res = await api.get(`/day-offs/${id}/report`, { responseType: 'blob' })
  const url = URL.createObjectURL(res.data)
  const a = document.createElement('a')
  a.href = url
  a.download = `report-${id}.docx`
  a.click()
  URL.revokeObjectURL(url)
}
