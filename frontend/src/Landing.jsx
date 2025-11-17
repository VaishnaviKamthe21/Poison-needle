import React, { useEffect, useState, useCallback } from "react";
import api from "./api";

function Landing() {
  const [products, setProducts] = useState([]);
  const [toasts, setToasts] = useState([]);
  const [loading, setLoading] = useState(false);

  const toast = useCallback((type, msg, title) => {
    const id = Date.now() + Math.random();
    setToasts((t) => [...t, { id, type, msg, title }]);
    setTimeout(() => setToasts((t) => t.filter((x) => x.id !== id)), 3000);
  }, []);

  const loadProducts = useCallback(async () => {
    try {
      setLoading(true);
      const r = await api.get("/products");
      setProducts(r.data || []);
    } catch (e) {
      setProducts([]);
      toast("danger", "Failed to load products", "Error");
      console.error(e?.response?.data || e);
    } finally {
      setLoading(false);
    }
  }, [toast]);

  useEffect(() => {
    loadProducts();
  }, [loadProducts]);

  const handleBuy = useCallback(
  async (p) => {
    const token = localStorage.getItem("token");
    if (!token) {
      window.alert("Please login to purchase"); // simple alert
      return;
    }
    try {
      await api.post(
        "/interactions/purchase",
        { items: [{ product_id: p.product_id, qty: 1 }] },
        { headers: { "Content-Type": "application/json" } }
      );
      window.alert("Order placed"); // simple alert
      await loadProducts();
    } catch (e) {
      const msg = e?.response?.data?.error || "Purchase failed";
      window.alert(msg); // simple alert
      console.error("Purchase error:", e?.response?.status, e?.response?.data, e);
    }
  },
  [loadProducts]
);


  return (
    <div className="container-fluid  flex-column justify-content-center align-items-center text-center landing-page py-4">
      <div className="text-center text-light mb-5">
        <h1>Poisons Needle</h1>
        <p className="lead">Handmade crochet gifts — minimal, soft, and heartfelt.</p>
      </div>

      <div className="toast-container">
        {toasts.map((t) => (
          <div key={t.id} className={`toast ${t.type}`}>
            {t.title && <div className="toast-title">{t.title}</div>}
            <div className="toast-msg">{t.msg}</div>
          </div>
        ))}
      </div>

      <h3 className="text-light mb-3">Best Sellers</h3>

      {loading && <div className="text-light">Loading...</div>}

      {!loading && (
        <div className="row py-2 px-5">
          {products.map((p) => (
            <div key={p.product_id} className="col-12 col-sm-6 col-md-4 mb-4">
              <div className="card p-3 h-100" style={{ background: "#2c2c2c", color: "#fff" }}>
                <div
                  style={{
                    height: 200,
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "center",
                    background: "#1f1f1f",
                    marginBottom: 12,
                    borderRadius: 8,
                  }}
                >
                  {p.image_url ? (
                    <img
                      src={p.image_url}
                      alt={p.name}
                      style={{ height: "100%", width: "100%", objectFit: "cover", borderRadius: 8 }}
                    />
                  ) : (
                    <span style={{ color: "#999" }}>Image</span>
                  )}
                </div>
                <h5>{p.name}</h5>
                <p>₹{Number(p.price).toFixed(0)}</p>
                <div className="d-flex justify-content-between">
                  <button className="btn btn-outline-light btn-sm">View</button>
                  <button
                    className="btn btn-primary btn-sm"
                    disabled={p.inventory_qty <= 0}
                    onClick={() => handleBuy(p)}
                  >
                    {p.inventory_qty > 0 ? "Buy" : "Out of stock"}
                  </button>
                </div>
              </div>
            </div>
          ))}
          {products.length === 0 && !loading && (
            <div className="text-light">No products yet.</div>
          )}
        </div>
      )}

      <footer className="text-center text-muted mt-5 mb-3">
        © {new Date().getFullYear()} Poisons Needle
      </footer>
    </div>
  );
}

export default Landing;
