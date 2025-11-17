import React, { useState } from "react";
import axios from "axios";

function Complaint() {
  const [formData, setFormData] = useState({
    name: "",
    email: "",
    product: "",
    issue: "",
  });

  const [alert, setAlert] = useState({ type: "", message: "" });

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      await axios.post("http://127.0.0.1:5000/complaint", formData);
      setAlert({ type: "success", message: "Your complaint has been submitted successfully!" });
      setFormData({ name: "", email: "", product: "", issue: "" });
    } catch (error) {
      setAlert({ type: "danger", message: "Error submitting complaint. Please try again." });
    }
  };

  return (
    <div className="container complaint-container">
      <h2 className="text-center mt-3" style={{ color: "#fff" }}>
        Submit a Complaint / Request
      </h2>

      {alert.message && (
        <div className={`alert alert-${alert.type} alert-dismissible fade show`} role="alert">
          {alert.message}
          <button type="button" className="btn-close" onClick={() => setAlert({ type: "", message: "" })}></button>
        </div>
      )}

      <form onSubmit={handleSubmit} className="text-start">
        <div className="mb-3">
          <label className="form-label">Name</label>
          <input type="text" className="form-control" name="name" value={formData.name} onChange={handleChange} required />
        </div>

        <div className="mb-3">
          <label className="form-label">Email</label>
          <input type="email" className="form-control" name="email" value={formData.email} onChange={handleChange} required />
        </div>

        <div className="mb-3">
          <label className="form-label">Product (optional)</label>
          <input type="text" className="form-control" name="product" value={formData.product} onChange={handleChange} />
        </div>

        <div className="mb-3">
          <label className="form-label">Issue / Complaint</label>
          <textarea className="form-control" name="issue" rows="4" value={formData.issue} onChange={handleChange} required />
        </div>

        <button type="submit" className="btn btn-primary">Submit</button>
      </form>
    </div>
  );
}

export default Complaint;
