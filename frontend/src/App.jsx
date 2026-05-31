import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import ProtectedRoute from './components/ProtectedRoute'
import Layout from './components/Layout'
import Login from './pages/Login'
import Register from './pages/Register'
import Dashboard from './pages/Dashboard'
import Overtimes from './pages/Overtimes'
import DayOffs from './pages/DayOffs'
import Profile from './pages/Profile'
import Statistics from './pages/Statistics'
import ModerationPage from './pages/ModerationPage'
import AdminPage from './pages/AdminPage'

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route
          path="/"
          element={
            <ProtectedRoute>
              <Layout />
            </ProtectedRoute>
          }
        >
          <Route index element={<Navigate to="/dashboard" replace />} />
          <Route path="dashboard" element={<Dashboard />} />
          <Route path="overtimes" element={<Overtimes />} />
          <Route path="day-offs" element={<DayOffs />} />
          <Route path="statistics" element={<Statistics />} />
          <Route
            path="moderation"
            element={
              <ProtectedRoute minRole="moderator">
                <ModerationPage />
              </ProtectedRoute>
            }
          />
          <Route
            path="admin"
            element={
              <ProtectedRoute minRole="admin">
                <AdminPage />
              </ProtectedRoute>
            }
          />
          <Route path="profile" element={<Profile />} />
        </Route>
        <Route path="*" element={<Navigate to="/dashboard" replace />} />
      </Routes>
    </BrowserRouter>
  )
}
