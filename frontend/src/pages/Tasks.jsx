import { useEffect, useState } from "react"
import api from "../api/axios"
import { useNavigate } from "react-router-dom"

const STATUS_LABELS = {
    pending: "Pending",
    in_progress: "In Progress",
    completed: "Completed",
}

const PRIORITY_ICONS = { low: "↓", medium: "→", high: "↑" }

export default function Tasks() {
    const [tasks, setTasks] = useState([])
    const [loading, setLoading] = useState(true)
    const navigate = useNavigate()

    useEffect(() => {
        api.get("/tasks/")
            .then(res => setTasks(res.data))
            .finally(() => setLoading(false))
    }, [])

    const handleDelete = async (id) => {
        await api.delete(`/tasks/${id}`)
        setTasks(tasks.filter(t => t.id !== id))
    }

    const handleLogout = () => {
        localStorage.removeItem("token")
        navigate("/login")
    }

    const counts = {
        total: tasks.length,
        pending: tasks.filter(t => t.status === "pending").length,
        in_progress: tasks.filter(t => t.status === "in_progress").length,
        completed: tasks.filter(t => t.status === "completed").length,
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
                        <button className="btn btn-ghost btn-sm" onClick={handleLogout}>
                            Sign out
                        </button>
                    </div>
                </div>
            </nav>

            <main className="page-content">
                <div className="page-header">
                    <div className="page-header-left">
                        <h1>My Tasks</h1>
                        <p>Manage and track your work</p>
                    </div>
                    <button className="btn btn-primary" onClick={() => navigate("/tasks/new")}>
                        + New Task
                    </button>
                </div>

                <div className="stats-bar">
                    <div className="stat-chip">
                        <div>
                            <div className="stat-chip-value">{counts.total}</div>
                            <div className="stat-chip-label">Total</div>
                        </div>
                    </div>
                    <div className="stat-chip">
                        <div>
                            <div className="stat-chip-value">{counts.pending}</div>
                            <div className="stat-chip-label">Pending</div>
                        </div>
                    </div>
                    <div className="stat-chip">
                        <div>
                            <div className="stat-chip-value">{counts.in_progress}</div>
                            <div className="stat-chip-label">In Progress</div>
                        </div>
                    </div>
                    <div className="stat-chip">
                        <div>
                            <div className="stat-chip-value">{counts.completed}</div>
                            <div className="stat-chip-label">Completed</div>
                        </div>
                    </div>
                </div>

                {loading ? (
                    <div className="tasks-empty">
                        <div className="tasks-empty-icon">⏳</div>
                        <h3>Loading tasks…</h3>
                    </div>
                ) : tasks.length === 0 ? (
                    <div className="tasks-empty">
                        <div className="tasks-empty-icon">📋</div>
                        <h3>No tasks yet</h3>
                        <p>Create your first task to get started</p>
                        <button className="btn btn-primary" onClick={() => navigate("/tasks/new")}>
                            + Create a task
                        </button>
                    </div>
                ) : (
                    <div className="tasks-grid">
                        {tasks.map(task => (
                            <div key={task.id} className="task-card">
                                <div className="task-card-header">
                                    <h3 className="task-card-title">{task.title}</h3>
                                    <button
                                        className="btn btn-danger btn-sm"
                                        onClick={() => handleDelete(task.id)}
                                        title="Delete task"
                                    >
                                        ✕
                                    </button>
                                </div>
                                {task.description && (
                                    <p className="task-card-desc">{task.description}</p>
                                )}
                                <div className="task-card-footer">
                                    <span className={`badge badge-${task.status}`}>
                                        {STATUS_LABELS[task.status] ?? task.status}
                                    </span>
                                    <span className={`badge badge-${task.priority}`}>
                                        {PRIORITY_ICONS[task.priority]} {task.priority}
                                    </span>
                                </div>
                            </div>
                        ))}
                    </div>
                )}
            </main>
        </div>
    )
}
