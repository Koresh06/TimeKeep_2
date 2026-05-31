import { Outlet } from 'react-router-dom'
import Navbar from './Navbar'

export default function Layout() {
  return (
    <div style={{ minHeight: '100vh' }}>
      <Navbar />
      <main
        className="page-enter"
        style={{
          maxWidth: 1520,
          margin: '0 auto',
          padding: '24px 32px 40px',
        }}
      >
        <Outlet />
      </main>
    </div>
  )
}
