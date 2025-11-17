# products.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from core import get_db

products_bp = Blueprint("products", __name__)

def is_admin():
    ident = get_jwt_identity()
    if not ident:
        return False
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT role FROM users WHERE user_id=%s", (int(ident),))
    row = cur.fetchone()
    db.close()
    return bool(row and row[0] == "admin")

@products_bp.get("")
def list_products():
    db = get_db()
    cur = db.cursor(dictionary=True)
    cur.execute("""
      SELECT p.*, GROUP_CONCAT(t.tag) AS tags
      FROM products p
      LEFT JOIN product_tags pt ON pt.product_id=p.product_id
      LEFT JOIN tags t ON t.tag_id=pt.tag_id
      WHERE p.is_active=1
      GROUP BY p.product_id
      ORDER BY p.created_at DESC
    """)
    rows = cur.fetchall()
    db.close()
    for r in rows:
        r["tags"] = r["tags"].split(",") if r["tags"] else []
    return jsonify(rows)

@products_bp.post("")
@jwt_required()
def create_product():
    if not is_admin():
        return jsonify({"error":"Forbidden"}), 403

    data = request.get_json(silent=True) or {}
    if not isinstance(data, dict):
        return jsonify({"error":"Expected JSON body"}), 400

    name = data.get("name")
    description = data.get("description","")
    price = data.get("price", 0.0)
    image_url = data.get("image_url","")
    try:
        inventory_qty = int(data.get("inventory_qty",0))
    except Exception:
        return jsonify({"error":"Invalid inventory"}), 400
    tags = [t.strip().lower() for t in data.get("tags",[])] if isinstance(data.get("tags",[]), list) else []

    if not name:
        return jsonify({"error":"Name required"}), 400

    db = get_db()
    cur = db.cursor()
    cur.execute(
        "INSERT INTO products(name,description,price,image_url,inventory_qty) VALUES (%s,%s,%s,%s,%s)",
        (name, description, price, image_url, inventory_qty)
    )
    pid = cur.lastrowid

    for t in tags:
        cur.execute("INSERT IGNORE INTO tags(tag) VALUES (%s)", (t,))
        cur.execute("SELECT tag_id FROM tags WHERE tag=%s", (t,))
        tag_id = cur.fetchone()[0]
        cur.execute("INSERT IGNORE INTO product_tags(product_id, tag_id) VALUES (%s,%s)", (pid, tag_id))

    db.commit(); db.close()
    return jsonify({"product_id": pid}), 201

@products_bp.put("/<int:pid>")
@jwt_required()
def update_product(pid):
    if not is_admin():
        return jsonify({"error":"Forbidden"}), 403

    data = request.get_json(silent=True) or {}
    if not isinstance(data, dict):
        return jsonify({"error":"Expected JSON body"}), 400

    fields=[]; vals=[]
    for col in ("name","description","price","image_url","inventory_qty","is_active"):
        if col in data:
            fields.append(f"{col}=%s"); vals.append(data[col])

    db = get_db()
    cur = db.cursor()

    if fields:
        cur.execute(f"UPDATE products SET {', '.join(fields)} WHERE product_id=%s", (*vals, pid))

    if "tags" in data:
        cur.execute("DELETE FROM product_tags WHERE product_id=%s", (pid,))
        for t in [x.strip().lower() for x in data.get("tags", [])]:
            cur.execute("INSERT IGNORE INTO tags(tag) VALUES (%s)", (t,))
            cur.execute("SELECT tag_id FROM tags WHERE tag=%s", (t,))
            tag_id = cur.fetchone()[0]
            cur.execute("INSERT IGNORE INTO product_tags(product_id, tag_id) VALUES (%s,%s)", (pid, tag_id))

    db.commit(); db.close()
    return jsonify({"message":"updated"})
