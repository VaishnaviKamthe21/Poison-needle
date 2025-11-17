import React, { useState, useContext } from "react";
import api from "./api";
import { useNavigate } from "react-router-dom";
import { AuthContext } from "./AuthContext";

export default function Register() {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [err, setErr] = useState("");
  const nav = useNavigate();
  const { login } = useContext(AuthContext);

  const onSubmit = async (e) => {
    e.preventDefault();
    try {
      const r = await api.post("/auth/register", { name, email, password });
      localStorage.setItem("token", r.data.access_token);
      await login(email, password); // hydrate auth state
      nav("/");
    } catch (ex) {
      setErr(ex?.response?.data?.error || "Error");
    }
  };

  return (
    <div className="container complaint-container">
      <h2>Register</h2>
      {err && <div className="alert alert-danger">{err}</div>}
      <form onSubmit={onSubmit}>
        <div className="mb-3">
          <label className="form-label">Name</label>
          <input className="form-control" value={name}
                 onChange={(e)=>setName(e.target.value)} required/>
        </div>
        <div className="mb-3">
          <label className="form-label">Email</label>
          <input className="form-control" type="email" value={email}
                 onChange={(e)=>setEmail(e.target.value)} required/>
        </div>
        <div className="mb-3">
          <label className="form-label">Password</label>
          <input className="form-control" type="password" value={password}
                 onChange={(e)=>setPassword(e.target.value)} required/>
        </div>
        <button className="btn btn-secondary" type="submit">Create Account</button>
      </form>
    </div>
  );
}
