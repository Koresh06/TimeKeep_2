import api from './axios'

export const getMe = () => api.get('/users/me')

export const getDepartmentUsers = (params = {}) =>
  api.get('/users/current-department', { params })

export const getOrganizationUsers = (params = {}) =>
  api.get('/users/current-organization', { params })

export const getAllUsers = (params = {}) =>
  api.get('/users', { params })

export const updateUserRole = (id, role) =>
  api.patch(`/users/${id}/role`, null, { params: { role } })

export const updateUserWorkMode = (id, work_mode) =>
  api.patch(`/users/${id}/work-mode`, null, { params: { work_mode } })

export const activateUser = (id, is_active) =>
  api.patch(`/users/${id}/activate`, null, { params: { is_active } })
