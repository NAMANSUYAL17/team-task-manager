import { Outlet, Link, useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'

export default function Layout() {
  const { user, logout } = useAuth()
  const navigate = useNavigate()

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <nav className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 py-3 flex items-center justify-between">
          <div className="flex items-center gap-8">
            <span className="text-xl font-bold text-indigo-600">TaskManager</span>
            <div className="flex gap-6">
              <Link to="/" className="text-gray-600 hover:text-indigo-600 font-medium">Dashboard</Link>
              <Link to="/projects" className="text-gray-600 hover:text-indigo-600 font-medium">Projects</Link>
              <Link to="/tasks" className="text-gray-600 hover:text-indigo-600 font-medium">Tasks</Link>
            </div>
          </div>
          <div className="flex items-center gap-4">
            <span className="text-gray-600 text-sm">👤 {user?.name}</span>
            <button
              onClick={handleLogout}
              className="bg-red-500 text-white px-4 py-1.5 rounded-lg text-sm hover:bg-red-600"
            >
              Logout
            </button>
          </div>
        </div>
      </nav>
      <main className="max-w-7xl mx-auto px-4 py-8">
        <Outlet />
      </main>
    </div>
  )
}