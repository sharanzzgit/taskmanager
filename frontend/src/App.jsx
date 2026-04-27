import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import Login from "./pages/Login";
import Register from "./pages/Register";
import Tasks from "./pages/Tasks";
import NewTask from "./pages/NewTask"
import EditTask from "./pages/EditTask";

function PrivateRoute({ children }) {
  return localStorage.getItem("token") ? children : <Navigate to="/login" replace />;
}

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Navigate to="/login" replace />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/tasks" element={<PrivateRoute><Tasks /></PrivateRoute>} />
        <Route path="/tasks/new" element={<PrivateRoute><NewTask /></PrivateRoute>} />
        <Route path="/tasks/:id/edit" element={<PrivateRoute><EditTask /></PrivateRoute>} />
      </Routes>
    </BrowserRouter>
  );
}