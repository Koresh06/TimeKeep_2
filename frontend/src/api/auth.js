import api from './axios'

export const login = (username, password) =>
  api.post('/auth/login', new URLSearchParams({ username, password }), {
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
  })

export const register = (data) => api.post('/auth/register', data)

export const getPublicOrganizations = () => api.get('/auth/organizations')

export const getPublicDepartments = (organizationId) =>
  api.get('/auth/departments', { params: { organization_id: organizationId } })
