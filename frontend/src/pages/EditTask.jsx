import { useEffect, useState } from "react"
import { useNavigate, useParams } from "react-router-dom"
import api from "../api/axios"

export default function EditTask() {
    const { id } = useParams()
    const navigate = useNavigate()
    const [form, setForm] = useState(null)
    const [loading, setLoading] = useState(true)
    const [saving, setSaving] = useState(false)
    const [error, setError] = useState("")

    useEffect(() => {
        api.get(`/tasks/${id}`)
            .then(res => setForm({
                title: res.data.title,
                description: res.data.description ?? "",
                status: res.data.status,
                priority: res.data.priority,
                due_date: res.data.due_date ? res.data.due_date.split("T")[0] : "",
            }))
            .catch(() => setError("Could not load task."))
            .finally(() => setLoading(false))
    }, [id])

    const handleChange = (e) => setForm({ ...form, [e.target.name]: e.target.value })

    const handleSave = async (e) => {
        e.preventDefault()
        if (!form.title.trim()) return
        setSaving(true)
        setError("")
        try {
            const payload = { ...form, due_date: form.due_date || null }
            await api.put(`/tasks/${id}`, payload)
            navigate("/tasks")
        } catch {
            setError("Failed to save changes. Please try again.")
        } finally {
            setSaving(false)
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
                        <h1>Edit Task</h1>
                        <p>Update the details of your task</p>
                    </div>
                </div>

                <div className="form-card">
                    <h2 className="form-card-title">Task details</h2>
                    <p className="form-card-subtitle">Make your changes and save</p>

                    {error && <div className="alert alert-error">{error}</div>}

                    {loading ? (
                        <div className="tasks-empty">
                            <div className="tasks-empty-icon">⏳</div>
                            <h3>Loading…</h3>
                        </div>
                    ) : form && (
                        <form onSubmit={handleSave}>
                            <div className="form-group">
                                <label className="form-label">Title</label>
                                <input
                                    className="form-input"
                                    name="title"
                                    value={form.title}
                                    onChange={handleChange}
                                    required
                                    autoFocus
                                />
                            </div>

                            <div className="form-group">
                                <label className="form-label">
                                    Description{" "}
                                    <span style={{ color: "var(--text-muted)", fontWeight: 400 }}>(optional)</span>
                                </label>
                                <textarea
                                    className="form-textarea"
                                    name="description"
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

                            <div className="form-group">
                                <label className="form-label">
                                    Due date{" "}
                                    <span style={{ color: "var(--text-muted)", fontWeight: 400 }}>(optional)</span>
                                </label>
                                <input
                                    className="form-input"
                                    type="date"
                                    name="due_date"
                                    value={form.due_date}
                                    onChange={handleChange}
                                />
                            </div>

                            <div className="form-actions">
                                <button type="submit" className="btn btn-primary" disabled={saving}>
                                    {saving ? "Saving…" : "Save changes"}
                                </button>
                                <button type="button" className="btn btn-ghost" onClick={() => navigate("/tasks")}>
                                    Cancel
                                </button>
                            </div>
                        </form>
                    )}
                </div>
            </main>
        </div>
    )
}
