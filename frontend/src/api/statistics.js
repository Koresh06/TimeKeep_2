import api from './axios'

export const getMyStatistics = () => api.get('/statistics/me')
export const getDepartmentStatistics = () => api.get('/statistics/current-department')
export const getOrganizationStatistics = () => api.get('/statistics/current-organization')
export const getAllStatistics = () => api.get('/statistics')
