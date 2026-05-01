import { useEffect, useState } from 'react'
import api from '../api/axios'

export default function ProjectsPage() {
  const [projects, setProjects] = useState([])
  const [form, setForm] = useState({ name: '', description: '' })
  const [loading, setLoading] = useState(false)
  const [showForm, setShowForm] = useState(false)

  const fetchProjects = () => {
    api.get('/api/projects/').then(res => setProjects(res.data))
  }

  useEffect(() => { fetchProjects() }, [])

  const handleCreate = async (e) => {
    e.preventDefault()
    setLoading(true)
    try {
      await api.post('/api/projects/', form)
      setForm({ name: '', description: '' })
      setShowForm(false)
      fetchProjects()
    } catch (err) {
      alert(err.response?.data?.detail || 'Failed to create project')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div>
      <div className="flex items-center justify-between mb-8">
        <h1 className="text-2xl font-bold text-gray-800">Projects</h1>
        <button
          onClick={() => setShowForm(!showForm)}
          className="bg-indigo-600 text-white px-4 py-2 rounded-lg hover:bg-indigo-700 font-medium"
        >
          + New Project
        </button>
      </div>

      {showForm && (
        <form onSubmit={handleCreate} className="bg-white rounded-xl shadow-sm p-6 mb-8 border border-gray-100">
          <h2 className="font-semibold text-gray-700 mb-4">Create New Project</h2>
          <div className="space-y-3">
            <input
              required
              placeholder="Project name"
              value={form.name}
              onChange={e => setForm({...form, name: e.target.value})}
              className="w-full border border-gray-300 rounded-lg px-4 py-2.5 focus:outline-none focus:ring-2 focus:ring-indigo-500"
            />
            <textarea
              placeholder="Description (optional)"
              value={form.description}
              onChange={e => setForm({...form, description: e.target.value})}
              className="w-full border border-gray-300 rounded-lg px-4 py-2.5 focus:outline-none focus:ring-2 focus:ring-indigo-500"
              rows={3}
            />
            <div className="flex gap-3">
              <button type="submit" disabled={loading}
                className="bg-indigo-600 text-white px-6 py-2 rounded-lg hover:bg-indigo-700 disabled:opacity-50">
                {loading ? 'Creating...' : 'Create'}
              </button>
              <button type="button" onClick={() => setShowForm(false)}
                className="border border-gray-300 text-gray-600 px-6 py-2 rounded-lg hover:bg-gray-50">
                Cancel
              </button>
            </div>
          </div>
        </form>
      )}

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {projects.map(p => (
          <div key={p.id} className="bg-white rounded-xl shadow-sm p-6 border border-gray-100 hover:shadow-md transition">
            <h3 className="font-semibold text-gray-800 text-lg">{p.name}</h3>
            <p className="text-gray-500 text-sm mt-1">{p.description || 'No description'}</p>
            <p className="text-xs text-gray-400 mt-4">
              Created {new Date(p.created_at).toLocaleDateString()}
            </p>
          </div>
        ))}
        {projects.length === 0 && (
          <p className="text-gray-400 col-span-3 text-center py-12">No projects yet. Create your first one!</p>
        )}
      </div>
    </div>
  )
}