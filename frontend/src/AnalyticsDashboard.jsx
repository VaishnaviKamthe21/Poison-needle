import React from "react";

export default function AnalyticsDashboard() {
  // Paste your actual embed URL below (not this demo link)
  const EMBED_URL =
    "https://app.powerbi.com/view?r=eyJrIjoiMTFjYjc5MDMtZTYxNC00ZTFmLWFhNWYtNWUyOWNlMGQ1NWY0IiwidCI6IjU1ZGJlOGQ0LTM3OGQtNDAwMy05NTc2LTBiODFhOWM0MmJhMiJ9";

  return (
    <div className="container analytics-dashboard">
      <h2 className="page-heading">Inventory Analytics Dashboard</h2>
      <div style={{borderRadius: "16px", overflow: "hidden", boxShadow: "0 1px 16px #252b3f33", textAlign: "center"}}>
        <iframe
          title="Power BI Analytics Dashboard"
          width="87%"
          height="700px"
          style={{minHeight: "500px", border: "none"}}
          src={EMBED_URL}
          allowFullScreen
        />
      </div>
    </div>
  );
}
