import api from './axios'

export const getMyOvertimes = () => api.get('/overtimes/me')
export const createOvertime = (data) => api.post('/overtimes', data)
