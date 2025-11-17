import React, { useState, useContext } from "react";
import { useNavigate } from "react-router-dom";
import { AuthContext } from "./AuthContext";

export default function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [err, setErr] = useState("");
  const nav = useNavigate();
  const { login } = useContext(AuthContext);

  const onSubmit = async (e) => {
    e.preventDefault();
    try {
      await login(email, password);
      nav("/");
    } catch (ex) {
      setErr(ex?.response?.data?.error || "Invalid credentials");
    }
  };

  return (
    <div className="container complaint-container">
      <h2>Login</h2>
      {err && <div className="alert alert-danger">{err}</div>}
      <form onSubmit={onSubmit}>
        <div className="mb-3">
          <label className="form-label">Email</label>
          <input className="form-control" type="email" value={email}
                 onChange={(e)=>setEmail(e.target.value)} required />
        </div>
        <div className="mb-3">
          <label className="form-label">Password</label>
          <input className="form-control" type="password" value={password}
                 onChange={(e)=>setPassword(e.target.value)} required />
        </div>
        <button className="btn btn-secondary" type="submit">Login</button>
      </form>
    </div>
  );
}
