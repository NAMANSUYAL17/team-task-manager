import { useEffect, useState } from 'react'
import api from '../api/axios'
import { useAuth } from '../context/AuthContext'

const StatCard = ({ label, value, color }) => (
  <div className={`bg-white rounded-xl shadow-sm p-6 border-l-4 ${color}`}>
    <p className="text-gray-500 text-sm font-medium">{label}</p>
    <p className="text-3xl font-bold text-gray-800 mt-1">{value}</p>
  </div>
)

export default function DashboardPage() {
  const { user } = useAuth()
  const [stats, setStats] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    api.get('/api/tasks/dashboard')
      .then(res => setStats(res.data))
      .catch(console.error)
      .finally(() => setLoading(false))
  }, [])

  return (
    <div>
      <h1 className="text-2xl font-bold text-gray-800 mb-1">
        Welcome back, {user?.name} 👋
      </h1>
      <p className="text-gray-500 mb-8">Here's your task overview</p>

      {loading ? (
        <div className="text-gray-400">Loading stats...</div>
      ) : (
        <div className="grid grid-cols-2 md:grid-cols-4 gap-6 mb-10">
          <StatCard label="Total Tasks" value={stats?.total ?? 0} color="border-indigo-500" />
          <StatCard label="To Do" value={stats?.todo ?? 0} color="border-gray-400" />
          <StatCard label="In Progress" value={stats?.in_progress ?? 0} color="border-yellow-400" />
          <StatCard label="Done" value={stats?.done ?? 0} color="border-green-500" />
        </div>
      )}

      {stats?.overdue > 0 && (
        <div className="bg-red-50 border border-red-200 rounded-xl p-4 text-red-700 font-medium">
          ⚠️ You have {stats.overdue} overdue task{stats.overdue > 1 ? 's' : ''}. Please review them.
        </div>
      )}
    </div>
  )
}