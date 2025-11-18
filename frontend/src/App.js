import React from "react";
import { BrowserRouter as Router, Routes, Route, Link, useNavigate } from "react-router-dom";
import Chatbot from "./Chatbot";
import Complaint from "./complaint";
import ViewComplaints from "./ViewComplaints";
import Landing from "./Landing";
import Login from "./Login";
import Register from "./Register";
import Restock from "./Restock";
import { AuthProvider, AuthContext } from "./AuthContext";
import AnalyticsDashboard from './AnalyticsDashboard';

function NavAuthButtons(){
  const nav = useNavigate();
  const { user, loading, logout } = React.useContext(AuthContext);

  if (loading) return null;

  return (
    <div style={{display:"inline-block"}}>
      {!user ? (
        <>
          <Link className="btn btn-secondary btn-sm me-2 nav-btn" to="/login">Login</Link>
          <Link className="btn btn-secondary btn-sm me-2 nav-btn" to="/register">Register</Link>
        </>
      ) : (
        <button className="btn btn-secondary btn-sm me-2 nav-btn" onClick={()=>{ logout(); nav("/"); }}>Logout</button>
      )}
    </div>
  );
}

function AppRoutes(){
  return (
    <div className="">
      <nav className="navbar navbar-dark bg-dark">
        <div className="container-fluid py-1">
          <Link className="navbar-brand" to="/">Poisons Needle</Link>
          <div>
            <Link className="btn btn-secondary btn-sm me-2 nav-btn" to="/">Home</Link>
            <Link className="btn btn-secondary btn-sm me-2 nav-btn" to="/chat">Chatbot</Link>
            <Link className="btn btn-secondary btn-sm me-2 nav-btn" to="/complaint">Submit</Link>
            <Link className="btn btn-secondary btn-sm me-2 nav-btn" to="/view">View Complaints</Link>
            <Link className="btn btn-secondary btn-sm me-2 nav-btn" to="/restock">Restock</Link>
            <Link className="btn btn-info btn-sm me-2 nav-btn" to="/analytics">Analytics</Link>

            <NavAuthButtons />
          </div>
        </div>
      </nav>

      <Routes>
        <Route path="/" element={<Landing />} />
        <Route path="/chat" element={<Chatbot />} />
        <Route path="/complaint" element={<Complaint />} />
        <Route path="/view" element={<ViewComplaints />} />
        <Route path="/restock" element={<Restock />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/analytics" element={<AnalyticsDashboard />} />
      </Routes>
    </div>
  );
}

export default function App(){
  return (
    <AuthProvider>
      <Router>
        <AppRoutes />
      </Router>
    </AuthProvider>
  );
}
