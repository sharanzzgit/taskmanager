import { useState } from "react"
import api from "../api/axios"
import { useNavigate } from "react-router-dom"

export default function Register() {
    const [form, setForm] = useState({ username: "", email: "", password: "" })
    const navigate = useNavigate()

    const handleChange = (e) => setForm({ ...form, [e.target.name]: e.target.value })

    const handleRegister = async () => {
        await api.post("/auth/register", form)
        navigate("/login")
    }

    return (
        <div>
            <h2>Register</h2>
            <input name="username" placeholder="Username" onChange={handleChange} />
            <input name="email" placeholder="Email" onChange={handleChange} />
            <input name="password" placeholder="Password" type="password" onChange={handleChange} />
            <button onClick={handleRegister}>Register</button>
            <p>Have an account? <a href="/login">Login</a></p>
        </div>
    )
}