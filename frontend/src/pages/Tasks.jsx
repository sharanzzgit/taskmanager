import { useEffect, useState } from "react"
import api from "../api/axios"
import { useNavigate } from "react-router-dom"

export default function Tasks() {
    const [tasks, setTasks] = useState([])
    const navigate = useNavigate()

    useEffect(() => {
        api.get("/tasks/").then(res => setTasks(res.data))
    }, [])

    const handleDelete = async (id) => {
        await api.delete(`/tasks/${id}`)
        setTasks(tasks.filter(t => t.id !== id))
    }

    return (
        <div>
            <h2>My Tasks</h2>
            <button onClick={() => navigate("/tasks/new")}>+ New Task</button>
            {tasks.map(task => (
                <div key={task.id}>
                    <h3>{task.title}</h3>
                    <p>{task.description}</p>
                    <p>{task.status} | {task.priority}</p>
                    <button onClick={() => handleDelete(task.id)}>Delete</button>
                </div>
            ))}
        </div>
    )
}