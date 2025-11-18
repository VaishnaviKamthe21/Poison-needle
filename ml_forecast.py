from flask import Blueprint, jsonify, request
from core import get_db
import pandas as pd
import numpy as np
from prophet import Prophet

ml_bp = Blueprint("ml", __name__)

def fetch_sales_and_products(days=365):
    db = get_db()
    cur = db.cursor(dictionary=True)
    cur.execute("""
      SELECT p.product_id, p.name, pr.created_at, pr.qty
      FROM purchases pr
      JOIN products p ON p.product_id = pr.product_id
      WHERE pr.created_at >= DATE_SUB(CURDATE(), INTERVAL %s DAY)
      ORDER BY pr.created_at ASC
    """, (days,))
    sales = cur.fetchall()
    cur.execute("SELECT product_id, name, inventory_qty FROM products WHERE is_active=1")
    products = cur.fetchall()
    db.close()
    return sales, products

def build_daily_series(sales, products):
    inv = {p["product_id"]: int(p["inventory_qty"]) for p in products}
    names = {p["product_id"]: p["name"] for p in products}
    if not sales:
        idx = pd.date_range(end=pd.Timestamp.today().normalize(), periods=30, freq="D")
        zero = pd.Series(np.zeros(len(idx)), index=idx)
        return {pid: zero for pid in inv}, inv, names
    df = pd.DataFrame(sales)
    df["ds"] = pd.to_datetime(df["created_at"]).dt.normalize()
    series = {}
    today = pd.Timestamp.today().normalize()
    for pid in inv.keys():
        dsub = df[df["product_id"] == pid]
        if dsub.empty:
            idx = pd.date_range(end=today, periods=30, freq="D")
            series[pid] = pd.Series(np.zeros(len(idx)), index=idx)
            continue
        s = dsub.groupby("ds")["qty"].sum()
        idx = pd.date_range(start=s.index.min(), end=today, freq="D")
        s = s.reindex(idx, fill_value=0.0)
        series[pid] = s.astype(float)
    return series, inv, names

def prophet_forecast(s: pd.Series, horizon=7):
    df = s.reset_index().rename(columns={"index": "ds", 0: "y", 1: "y"})
    df['ds'] = pd.to_datetime(df['ds'])
    m = Prophet(weekly_seasonality=True)
    m.fit(df)
    future = m.make_future_dataframe(periods=horizon)
    forecast = m.predict(future)
    last_h = forecast.tail(horizon)
    p50 = last_h['yhat'].sum()
    p90 = last_h['yhat_upper'].sum() * 1.1  # slight up-scaling for uncertainty
    return p50, p90

def moving_average_forecast(s: pd.Series, horizon=7):
    n = len(s)
    if n == 0:
        base = 0.0
    elif n < 7:
        base = float(s.mean())
    else:
        base = float(s.tail(7).mean())
    p50 = base * horizon
    p90 = p50 * 1.2
    return p50, p90

@ml_bp.get("/ml/restock-plan")
def restock_plan():
    horizon = int(request.args.get("h", 7))
    sales, products = fetch_sales_and_products(days=365)
    series, inv, names = build_daily_series(sales, products)

    out = []
    for pid, s in series.items():
        # Choose model based on history length
        if len(s) >= 14:
            try:
                p50_7d, p90_7d = prophet_forecast(s, horizon=horizon)
                model_used = "Prophet"
            except Exception:
                p50_7d, p90_7d = moving_average_forecast(s, horizon=horizon)
                model_used = "MovingAverage"
        else:
            p50_7d, p90_7d = moving_average_forecast(s, horizon=horizon)
            model_used = "MovingAverage"
        current = inv.get(pid, 0)
        recent7 = int(s.tail(7).sum()) if len(s) >= 7 else int(s.sum())
        safety = max(0.0, p90_7d - p50_7d)
        restock = int(max(0, round(p90_7d - current)))
        out.append({
            "product_id": int(pid),
            "name": names.get(pid, str(pid)),
            "inventory_qty": int(current),
            "recent7d_sales": recent7,
            "p50_7d": round(p50_7d, 2),
            "p90_7d": round(p90_7d, 2),
            "safety_stock": round(safety, 2),
            "suggested_restock": restock,
            "model_used": model_used
        })
    out.sort(key=lambda x: x["suggested_restock"], reverse=True)
    return jsonify(out)
