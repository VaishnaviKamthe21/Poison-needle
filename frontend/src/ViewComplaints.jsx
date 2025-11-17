import React, { useEffect, useState } from "react";
import axios from "axios";

function ViewComplaints() {
  const [complaints, setComplaints] = useState([]);

  useEffect(() => {
    axios.get("http://127.0.0.1:5000/view_complaints")
      .then((res) => setComplaints(res.data))
      .catch((err) => console.error(err));
  }, []);

  return (
    <div className="container viewcomplaints-container px-5">
      <h2 className="page-heading">Submitted Complaints</h2>
      <div className="table-responsive">
        <table className="complaint-table">
          <thead>
            <tr>
              <th>ID</th><th>Name</th><th>Email</th><th>Product</th><th>Issue</th><th>Submitted At</th>
            </tr>
          </thead>
          <tbody>
            {complaints.length === 0 && <tr><td colSpan="6" style={{textAlign:'center'}}>No complaints yet.</td></tr>}
            {complaints.map((c) => (
              <tr key={c.id}>
                <td>{c.complaint_id}</td>
                <td>{c.name}</td>
                <td>{c.email}</td>
                <td>{c.product}</td>
                <td style={{whiteSpace: 'pre-wrap'}}>{c.issue}</td>
                <td>{c.created_at}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default ViewComplaints;
