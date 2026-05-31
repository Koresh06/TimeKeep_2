import { Navigate } from 'react-router-dom'
import { useAuth, hasRole } from '../context/AuthContext'

export default function ProtectedRoute({ children, minRole }) {
  const { token, tokenData } = useAuth()

  if (!token) return <Navigate to="/login" replace />
  if (minRole && !hasRole(tokenData, minRole)) return <Navigate to="/dashboard" replace />

  return children
}
