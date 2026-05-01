import { useEffect, useState } from 'react'
import api from '../api/axios'

const statusColors = {
  todo: 'bg-gray-100 text-gray-700',
  in_progress: 'bg-yellow-100 text-yellow-700',
  done: 'bg-green-100 text-green-700',
}

const priorityColors = {
  low: 'bg-blue-100 text-blue-700',
  medium: 'bg-orange-100 text-orange-700',
  high: 'bg-red-100 text-red-700',
}

export default function TasksPage() {
  const [tasks, setTasks] = useState([])
  const [projects, setProjects] = useState([])
  const [showForm, setShowForm] = useState(false)
  const [form, setForm] = useState({ title: '', description: '', project_id: '', priority: 'medium', due_date: '' })
  const [loading, setLoading] = useState(false)

  const fetchAll = () => {
    api.get('/api/tasks/').then(res => setTasks(res.data))
    api.get('/api/projects/').then(res => setProjects(res.data))
  }

  useEffect(() => { fetchAll() }, [])

  const handleCreate = async (e) => {
    e.preventDefault()
    setLoading(true)
    try {
      await api.post('/api/tasks/', {
        ...form,
        project_id: parseInt(form.project_id),
        due_date: form.due_date || null,
      })
      setForm({ title: '', description: '', project_id: '', priority: 'medium', due_date: '' })
      setShowForm(false)
      fetchAll()
    } catch (err) {
      alert(err.response?.data?.detail || 'Failed to create task')
    } finally {
      setLoading(false)
    }
  }

  const updateStatus = async (taskId, status) => {
    try {
      await api.patch(`/api/tasks/${taskId}/status?status=${status}`)
      fetchAll()
    } catch (err) {
      alert('Failed to update status')
    }
  }

  return (
    <div>
      <div className="flex items-center justify-between mb-8">
        <h1 className="text-2xl font-bold text-gray-800">Tasks</h1>
        <button
          onClick={() => setShowForm(!showForm)}
          className="bg-indigo-600 text-white px-4 py-2 rounded-lg hover:bg-indigo-700 font-medium"
        >
          + New Task
        </button>
      </div>

      {showForm && (
        <form onSubmit={handleCreate} className="bg-white rounded-xl shadow-sm p-6 mb-8 border border-gray-100">
          <h2 className="font-semibold text-gray-700 mb-4">Create New Task</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <input required placeholder="Task title" value={form.title}
              onChange={e => setForm({...form, title: e.target.value})}
              className="border border-gray-300 rounded-lg px-4 py-2.5 focus:outline-none focus:ring-2 focus:ring-indigo-500" />
            <select required value={form.project_id}
              onChange={e => setForm({...form, project_id: e.target.value})}
              className="border border-gray-300 rounded-lg px-4 py-2.5 focus:outline-none focus:ring-2 focus:ring-indigo-500">
              <option value="">Select Project</option>
              {projects.map(p => <option key={p.id} value={p.id}>{p.name}</option>)}
            </select>
            <select value={form.priority} onChange={e => setForm({...form, priority: e.target.value})}
              className="border border-gray-300 rounded-lg px-4 py-2.5 focus:outline-none focus:ring-2 focus:ring-indigo-500">
              <option value="low">Low Priority</option>
              <option value="medium">Medium Priority</option>
              <option value="high">High Priority</option>
            </select>
            <input type="date" value={form.due_date}
              onChange={e => setForm({...form, due_date: e.target.value})}
              className="border border-gray-300 rounded-lg px-4 py-2.5 focus:outline-none focus:ring-2 focus:ring-indigo-500" />
            <textarea placeholder="Description (optional)" value={form.description}
              onChange={e => setForm({...form, description: e.target.value})}
              className="border border-gray-300 rounded-lg px-4 py-2.5 focus:outline-none focus:ring-2 focus:ring-indigo-500 md:col-span-2"
              rows={2} />
          </div>
          <div className="flex gap-3 mt-4">
            <button type="submit" disabled={loading}
              className="bg-indigo-600 text-white px-6 py-2 rounded-lg hover:bg-indigo-700 disabled:opacity-50">
              {loading ? 'Creating...' : 'Create Task'}
            </button>
            <button type="button" onClick={() => setShowForm(false)}
              className="border border-gray-300 text-gray-600 px-6 py-2 rounded-lg hover:bg-gray-50">
              Cancel
            </button>
          </div>
        </form>
      )}

      <div className="space-y-4">
        {tasks.map(task => (
          <div key={task.id} className="bg-white rounded-xl shadow-sm p-5 border border-gray-100 flex items-center justify-between">
            <div className="flex-1">
              <div className="flex items-center gap-3 mb-1">
                <h3 className="font-semibold text-gray-800">{task.title}</h3>
                <span className={`text-xs px-2 py-0.5 rounded-full font-medium ${priorityColors[task.priority]}`}>
                  {task.priority}
                </span>
              </div>
              <p className="text-gray-500 text-sm">{task.description}</p>
              {task.due_date && (
                <p className="text-xs text-gray-400 mt-1">
                  Due: {new Date(task.due_date).toLocaleDateString()}
                </p>
              )}
            </div>
            <div className="ml-6">
              <select
                value={task.status}
                onChange={e => updateStatus(task.id, e.target.value)}
                className={`text-sm px-3 py-1.5 rounded-full font-medium border-0 cursor-pointer ${statusColors[task.status]}`}
              >
                <option value="todo">To Do</option>
                <option value="in_progress">In Progress</option>
                <option value="done">Done</option>
              </select>
            </div>
          </div>
        ))}
        {tasks.length === 0 && (
          <p className="text-gray-400 text-center py-12">No tasks yet. Create your first task!</p>
        )}
      </div>
    </div>
  )
}