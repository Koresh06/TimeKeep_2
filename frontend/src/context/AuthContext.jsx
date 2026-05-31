import { createContext, useCallback, useContext, useState } from 'react'

function decodeToken(token) {
  try {
    return JSON.parse(atob(token.split('.')[1]))
  } catch {
    return null
  }
}

const AuthContext = createContext(null)

export function AuthProvider({ children }) {
  const [token, setToken] = useState(() => localStorage.getItem('token'))
  const tokenData = token ? decodeToken(token) : null

  const saveToken = useCallback((t) => {
    localStorage.setItem('token', t)
    setToken(t)
  }, [])

  const logout = useCallback(() => {
    localStorage.removeItem('token')
    setToken(null)
  }, [])

  return (
    <AuthContext.Provider value={{ token, tokenData, saveToken, logout }}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  return useContext(AuthContext)
}

// Role hierarchy helpers
const ROLE_LEVEL = { user: 1, moderator: 2, admin: 3, super_admin: 4 }

export function hasRole(tokenData, minRole) {
  if (!tokenData?.role) return false
  return (ROLE_LEVEL[tokenData.role] || 0) >= (ROLE_LEVEL[minRole] || 0)
}
