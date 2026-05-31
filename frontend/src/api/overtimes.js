import api from './axios'

export const getMyOvertimes = (params = {}) =>
  api.get('/overtimes/me', { params })

export const getDepartmentOvertimes = (params = {}) =>
  api.get('/overtimes/current-department', { params })

export const getOrganizationOvertimes = (params = {}) =>
  api.get('/overtimes/current-organization', { params })

export const getAllOvertimes = (params = {}) =>
  api.get('/overtimes', { params })

export const createOvertime = (form) =>
  api.post('/overtimes', {
    date_: form.date,
    start_time: form.start_time.length === 5 ? form.start_time + ':00' : form.start_time,
    end_time: form.end_time.length === 5 ? form.end_time + ':00' : form.end_time,
    description: form.description || '',
  })

export const deleteOvertime = (id) => api.delete(`/overtimes/${id}`)
