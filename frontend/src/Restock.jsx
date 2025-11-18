import React, { useEffect, useState } from "react";
import api from "./api";

export default function Restock(){
  const [rows, setRows] = useState([]);
  const [loading, setLoading] = useState(false);
  const [err, setErr] = useState("");

  useEffect(()=>{
    (async()=>{
      try{
        setLoading(true);
        const r = await api.get("/ml/restock-plan?h=7");
        setRows(r.data || []);
      }catch(e){
        setErr(e?.response?.data?.error || "Failed to load restock plan");
      }finally{
        setLoading(false);
      }
    })();
  },[]);

  return (
    <div className="container viewcomplaints-container">
      <h2 className="page-heading">Restock Planner (7 days)</h2>
      {err && <div className="alert alert-danger">{err}</div>}
      {loading && <div className="text-light">Loading...</div>}

      {!loading && (
        <div className="table-responsive">
          <table className="complaint-table">
            <thead>
              <tr>
                <th>Product</th>
                <th>Inventory</th>
                <th>P50 (7d)</th>
                <th>P90 (7d)</th>
                <th>Safety</th>
                <th>Suggested Restock</th>
              </tr>
            </thead>
            <tbody>
              {rows.length === 0 && (
                <tr><td colSpan="6" style={{textAlign:'center'}}>No data yet.</td></tr>
              )}
              {rows.map((r)=>(
                <tr key={r.product_id}>
                  <td>{r.name}</td>
                  <td>{r.inventory_qty}</td>
                  <td>{r.p50_7d}</td>
                  <td>{r.p90_7d}</td>
                  <td>{r.safety_stock}</td>
                  <td style={{ fontWeight: 600, color: r.suggested_restock > 0 ? "#ffc107" : "#28a745" }}>
                    {r.suggested_restock}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
