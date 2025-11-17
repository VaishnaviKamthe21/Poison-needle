# ml_forecast.py
from flask import Blueprint, jsonify, request
from core import get_db
import pandas as pd
import numpy as np

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
        # return zero series for all products
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

def moving_average_forecast(s: pd.Series, horizon=7):
    n = len(s)
    # if little history, fallback to simple mean of whatever we have
    if n == 0:
        base = 0.0
    elif n < 7:
        base = float(s.mean())
    else:
        base = float(s.tail(7).mean())  # last 7-day average
    p50 = base * horizon
    p90 = p50 * 1.2  # simple safety buffer (20%)
    return round(p50, 2), round(p90, 2)

@ml_bp.get("/ml/restock-plan")
def restock_plan():
    horizon = int(request.args.get("h", 7))
    sales, products = fetch_sales_and_products(days=365)
    series, inv, names = build_daily_series(sales, products)

    out = []
    for pid, s in series.items():
        p50_7d, p90_7d = moving_average_forecast(s, horizon=horizon)
        current = inv.get(pid, 0)
        safety = max(0.0, p90_7d - p50_7d)
        need = p90_7d + safety - current
        restock = int(max(0, round(need)))
        out.append({
            "product_id": int(pid),
            "name": names.get(pid, str(pid)),
            "inventory_qty": int(current),
            "p50_7d": p50_7d,
            "p90_7d": p90_7d,
            "safety_stock": round(safety,2),
            "suggested_restock": restock
        })

    out.sort(key=lambda x: x["suggested_restock"], reverse=True)
    return jsonify(out)
