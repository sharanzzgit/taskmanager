import { useState } from "react"
import api from "../api/axios"
import { useNavigate } from "react-router-dom"

export default function Login() {
    const [email, setEmail] = useState("")
    const [password, setPassword] = useState("")
    const navigate = useNavigate()

    const handleLogin = async () => {
        const form = new FormData()
        form.append("username", email)
        form.append("password", password)
        const res = await api.post("/auth/login", form)
        localStorage.setItem("token", res.data.access_token)
        navigate("/tasks")
    }

    return (
        <div>
            <h2>Login</h2>
            <input placeholder="Email" onChange={e => setEmail(e.target.value)} />
            <input placeholder="Password" type="password" onChange={e => setPassword(e.target.value)} />
            <button onClick={handleLogin}>Login</button>
            <p>No account? <a href="/register">Register</a></p>
        </div>
    )
}