import { useState } from "react"
import api from "../api/axios"
import { useNavigate } from "react-router-dom"

export default function NewTask() {
    const [form, setForm] = useState({ title: "", description: "", status: "pending", priority: "low" })
    const navigate = useNavigate()

    const handleChange = (e) => setForm({ ...form, [e.target.name]: e.target.value })

    const handleCreate = async () => {
        await api.post("/tasks/", form)
        navigate("/tasks")
    }

    return (
        <div>
            <h2>Create Task</h2>
            <input name="title" placeholder="Title" onChange={handleChange} />
            <input name="description" placeholder="Description" onChange={handleChange} />
            <select name="status" onChange={handleChange}>
                <option value="pending">Pending</option>
                <option value="in_progress">In Progress</option>
                <option value="completed">Completed</option>
            </select>
            <select name="priority" onChange={handleChange}>
                <option value="low">Low</option>
                <option value="medium">Medium</option>
                <option value="high">High</option>
            </select>
            <button onClick={handleCreate}>Create</button>
        </div>
    )
}