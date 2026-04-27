import { useState } from "react"
import api from "../api/axios"
import { useNavigate } from "react-router-dom"

export default function NewTask() {
    const [form, setForm] = useState({ title: "", description: "", status: "pending", priority: "low" })
    const [loading, setLoading] = useState(false)
    const [error, setError] = useState("")
    const navigate = useNavigate()

    const handleChange = (e) => setForm({ ...form, [e.target.name]: e.target.value })

    const handleCreate = async (e) => {
        e.preventDefault()
        if (!form.title.trim()) return
        setLoading(true)
        setError("")
        try {
            await api.post("/tasks/", form)
            navigate("/tasks")
        } catch {
            setError("Failed to create task. Please try again.")
        } finally {
            setLoading(false)
        }
    }

    return (
        <div className="app-layout">
            <nav className="navbar">
                <div className="navbar-inner">
                    <a className="navbar-brand" href="/tasks">
                        <div className="navbar-brand-icon">✓</div>
                        <span className="navbar-brand-name">TaskFlow</span>
                    </a>
                    <div className="navbar-actions">
                        <button className="btn btn-ghost btn-sm" onClick={() => navigate("/tasks")}>
                            ← Back to tasks
                        </button>
                    </div>
                </div>
            </nav>

            <main className="page-content">
                <div className="page-header">
                    <div className="page-header-left">
                        <h1>New Task</h1>
                        <p>Add a task to your list</p>
                    </div>
                </div>

                <div className="form-card">
                    <h2 className="form-card-title">Task details</h2>
                    <p className="form-card-subtitle">Fill in the information below to create your task</p>

                    {error && <div className="alert alert-error">{error}</div>}

                    <form onSubmit={handleCreate}>
                        <div className="form-group">
                            <label className="form-label">Title</label>
                            <input
                                className="form-input"
                                name="title"
                                placeholder="What needs to be done?"
                                value={form.title}
                                onChange={handleChange}
                                required
                                autoFocus
                            />
                        </div>

                        <div className="form-group">
                            <label className="form-label">Description <span style={{ color: 'var(--text-muted)', fontWeight: 400 }}>(optional)</span></label>
                            <textarea
                                className="form-textarea"
                                name="description"
                                placeholder="Add more details about this task…"
                                value={form.description}
                                onChange={handleChange}
                            />
                        </div>

                        <div className="form-row">
                            <div className="form-group">
                                <label className="form-label">Status</label>
                                <select className="form-select" name="status" value={form.status} onChange={handleChange}>
                                    <option value="pending">Pending</option>
                                    <option value="in_progress">In Progress</option>
                                    <option value="completed">Completed</option>
                                </select>
                            </div>

                            <div className="form-group">
                                <label className="form-label">Priority</label>
                                <select className="form-select" name="priority" value={form.priority} onChange={handleChange}>
                                    <option value="low">Low</option>
                                    <option value="medium">Medium</option>
                                    <option value="high">High</option>
                                </select>
                            </div>
                        </div>

                        <div className="form-actions">
                            <button type="submit" className="btn btn-primary" disabled={loading}>
                                {loading ? "Creating…" : "Create task"}
                            </button>
                            <button type="button" className="btn btn-ghost" onClick={() => navigate("/tasks")}>
                                Cancel
                            </button>
                        </div>
                    </form>
                </div>
            </main>
        </div>
    )
}