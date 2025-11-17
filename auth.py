# auth.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from email_validator import validate_email, EmailNotValidError
from datetime import timedelta

from core import bcrypt, get_db

auth_bp = Blueprint("auth", __name__)

@auth_bp.post("/register")
def register():
    data = request.get_json() or {}
    name = (data.get("name") or "").strip()
    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""

    if not name or not email or not password:
        return jsonify({"error": "Missing fields"}), 400

    try:
        validate_email(email)
    except EmailNotValidError:
        return jsonify({"error": "Invalid email"}), 400

    if len(password) < 8:
        return jsonify({"error": "Password too short"}), 400

    db = get_db()
    cur = db.cursor(dictionary=True)
    cur.execute("SELECT user_id FROM users WHERE email=%s", (email,))
    if cur.fetchone():
        db.close()
        return jsonify({"error": "Email already registered"}), 409

    pw_hash = bcrypt.generate_password_hash(password).decode("utf-8")
    cur.execute(
        "INSERT INTO users(name, email, password_hash, role) VALUES (%s, %s, %s, %s)",
        (name, email, pw_hash, "user"),
    )
    uid = cur.lastrowid

    cur.execute(
        "INSERT INTO user_preferences(user_id, preferred_tags, color_prefs, size_prefs) VALUES (%s, %s, %s, %s)",
        (uid, None, None, None),
    )

    db.commit()
    db.close()

    # Use simple identity = user_id as string
    token = create_access_token(identity=str(uid), expires_delta=timedelta(hours=12))
    return jsonify({"access_token": token}), 201


@auth_bp.post("/login")
def login():
    data = request.get_json() or {}
    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""

    db = get_db()
    cur = db.cursor(dictionary=True)
    cur.execute("SELECT user_id, name, role, password_hash FROM users WHERE email=%s", (email,))
    row = cur.fetchone()
    db.close()

    if not row:
        return jsonify({"error": "Invalid credentials"}), 401

    if not bcrypt.check_password_hash(row["password_hash"], password):
        return jsonify({"error": "Invalid credentials"}), 401

    # Use simple identity = user_id as string
    token = create_access_token(identity=str(row["user_id"]), expires_delta=timedelta(hours=12))
    return jsonify({"access_token": token})


@auth_bp.get("/me")
@jwt_required()
def me():
    user_id = get_jwt_identity()  # string user_id from token

    db = get_db()
    cur = db.cursor(dictionary=True)

    cur.execute("SELECT user_id, name, email, role, created_at FROM users WHERE user_id=%s", (user_id,))
    user = cur.fetchone()

    cur.execute("SELECT preferred_tags, color_prefs, size_prefs FROM user_preferences WHERE user_id=%s", (user_id,))
    prefs = cur.fetchone() or {}

    db.close()

    return jsonify({"user": user, "preferences": prefs})
