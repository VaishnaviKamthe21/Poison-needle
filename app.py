# app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import os

from chatbot import get_response
from core import bcrypt, jwt, get_db  

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "change_this_very_long_random_secret")

from flask_cors import CORS

CORS(
    app,
    resources={r"/*": {"origins": ["http://localhost:3000", "http://127.0.0.1:3000"]}},
    methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"],
    expose_headers=["Authorization"],
    supports_credentials=False,
)


# Initialize extensions with app here
bcrypt.init_app(app)
jwt.init_app(app)

from flask import jsonify
from flask_jwt_extended import JWTManager

# ... existing init
jwt = JWTManager(app)

from flask import jsonify
from flask_jwt_extended import JWTManager

@jwt.unauthorized_loader
def custom_unauth(err_str):
    return jsonify({"error": f"Unauthorized: {err_str}"}), 401

@jwt.invalid_token_loader
def custom_invalid(err_str):
    return jsonify({"error": f"Invalid token: {err_str}"}), 422

@jwt.expired_token_loader
def custom_expired(jwt_header, jwt_payload):
    return jsonify({"error": "Token expired"}), 401



# Chatbot API
@app.route('/get_response', methods=['POST'])
def get_bot_response():
    data = request.get_json()
    user_message = data.get('message', '')
    bot_reply = get_response(user_message)
    return jsonify({'reply': bot_reply})

# Complaint submission
@app.route('/complaint', methods=['POST'])
def submit_complaint():
    data = request.get_json()
    name = data.get('name', '')
    email = data.get('email', '')
    product = data.get('product', '')
    issue = data.get('issue', '')

    if not name or not email or not issue:
        return jsonify({'error': 'Missing required fields'}), 400

    db = get_db()
    cur = db.cursor()
    cur.execute(
        "INSERT INTO complaints (name, email, issue, product) VALUES (%s, %s, %s, %s)",
        (name, email, issue, product)
    )
    db.commit()
    db.close()
    return jsonify({'message': 'Complaint submitted successfully!'})

# View complaints
@app.route('/view_complaints', methods=['GET'])
def view_complaints():
    db = get_db()
    cur = db.cursor(dictionary=True)
    cur.execute("SELECT * FROM complaints ORDER BY complaint_id DESC")
    complaints = cur.fetchall()
    db.close()
    return jsonify(complaints)

# Register blueprints AFTER app and extensions are ready
from auth import auth_bp
app.register_blueprint(auth_bp, url_prefix="/auth")

from products import products_bp
app.register_blueprint(products_bp, url_prefix="/products")

from interactions import interactions_bp
app.register_blueprint(interactions_bp, url_prefix="/interactions")

from ml_forecast import ml_bp
app.register_blueprint(ml_bp, url_prefix="")


if __name__ == '__main__':
    app.run(debug=True, host="127.0.0.1", port=5000)
