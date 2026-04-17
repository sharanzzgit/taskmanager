import { useState } from "react"
import api from "../api/axios"
import { useNavigate } from "react-router-dom"

export default function Register() {
    const [form, setForm] = useState({ username: "", email: "", password: "" })
    const [error, setError] = useState("")
    const [loading, setLoading] = useState(false)
    const navigate = useNavigate()

    const handleChange = (e) => setForm({ ...form, [e.target.name]: e.target.value })

    const handleRegister = async (e) => {
        e.preventDefault()
        setError("")
        setLoading(true)
        try {
            await api.post("/auth/register", form)
            navigate("/login")
        } catch {
            setError("Registration failed. The email may already be in use.")
        } finally {
            setLoading(false)
        }
    }

    return (
        <div className="auth-page">
            <div className="auth-card">
                <div className="auth-logo">
                    <div className="auth-logo-icon">✓</div>
                    <span className="auth-logo-text">TaskFlow</span>
                </div>

                <h1 className="auth-title">Create an account</h1>
                <p className="auth-subtitle">Start managing your tasks for free</p>

                {error && <div className="alert alert-error">{error}</div>}

                <form onSubmit={handleRegister}>
                    <div className="form-group">
                        <label className="form-label">Username</label>
                        <input
                            className="form-input"
                            name="username"
                            placeholder="johndoe"
                            value={form.username}
                            onChange={handleChange}
                            required
                        />
                    </div>

                    <div className="form-group">
                        <label className="form-label">Email address</label>
                        <input
                            className="form-input"
                            name="email"
                            type="email"
                            placeholder="you@example.com"
                            value={form.email}
                            onChange={handleChange}
                            required
                        />
                    </div>

                    <div className="form-group">
                        <label className="form-label">Password</label>
                        <input
                            className="form-input"
                            name="password"
                            type="password"
                            placeholder="Create a strong password"
                            value={form.password}
                            onChange={handleChange}
                            required
                        />
                    </div>

                    <button
                        type="submit"
                        className="btn btn-primary btn-full"
                        disabled={loading}
                        style={{ marginTop: 8 }}
                    >
                        {loading ? "Creating account…" : "Create account"}
                    </button>
                </form>

                <p className="auth-footer">
                    Already have an account?{" "}
                    <a href="/login">Sign in</a>
                </p>
            </div>
        </div>
    )
}
