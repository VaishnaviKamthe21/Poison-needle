from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from core import get_db

interactions_bp = Blueprint("interactions", __name__)

@interactions_bp.post("")
@jwt_required(optional=True)
def log_interaction():
    ident = get_jwt_identity()
    data = request.get_json(silent=True) or {}
    if not isinstance(data, dict):
        return jsonify({"error": "Expected JSON body"}), 400

    product_id = int(data.get("product_id", 0)) if str(data.get("product_id", "0")).isdigit() else 0
    itype = data.get("type")
    if not product_id or itype not in ("view", "cart", "wishlist"):
        return jsonify({"error": "Invalid"}), 400

    db = get_db()
    cur = db.cursor()
    cur.execute(
        "INSERT INTO interactions(user_id,product_id,type) VALUES (%s,%s,%s)",
        (ident["user_id"] if ident else None, product_id, itype)
    )
    db.commit(); db.close()
    return jsonify({"message": "ok"}), 201

@interactions_bp.post("/purchase")
@jwt_required()
def purchase():
    user_id = int(get_jwt_identity())

    data = request.get_json(silent=True) or {}
    if not isinstance(data, dict):
        return jsonify({"error": "Expected JSON body"}), 400

    items = data.get("items", [])
    if not isinstance(items, list) or len(items) == 0:
        return jsonify({"error": "No items"}), 400

    db = get_db()
    cur = db.cursor(dictionary=True)
    try:
        db.start_transaction()
        for it in items:
            if not isinstance(it, dict) or "product_id" not in it or "qty" not in it:
                db.rollback(); db.close()
                return jsonify({"error": "Invalid item"}), 400

            try:
                pid = int(it["product_id"]); qty = int(it["qty"])
            except Exception:
                db.rollback(); db.close()
                return jsonify({"error": "Invalid quantity or product id"}), 400

            if qty <= 0:
                db.rollback(); db.close()
                return jsonify({"error": "Quantity must be positive"}), 400

            cur.execute("SELECT price, inventory_qty FROM products WHERE product_id=%s FOR UPDATE", (pid,))
            row = cur.fetchone()
            if not row:
                db.rollback(); db.close()
                return jsonify({"error": "Product not found"}), 404
            if row["inventory_qty"] < qty:
                db.rollback(); db.close()
                return jsonify({"error": "Insufficient inventory"}), 400

            cur.execute(
                "INSERT INTO purchases(user_id,product_id,qty,price_at_purchase) VALUES (%s,%s,%s,%s)",
                (user_id, pid, qty, row["price"])
            )
            cur.execute("UPDATE products SET inventory_qty = inventory_qty - %s WHERE product_id=%s", (qty, pid))

        db.commit(); db.close()
        return jsonify({"message": "Success"}), 201

    except Exception as e:
        db.rollback(); db.close()
        return jsonify({"error": f"Failed: {str(e)}"}), 500
