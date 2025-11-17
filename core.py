# core.py
import os
import mysql.connector
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

bcrypt = Bcrypt()
jwt = JWTManager()

DB_HOST = "localhost"
DB_USER = "root"
DB_PASS = "root"
DB_NAME = "chatbot_project"

def get_db():
    return mysql.connector.connect(
        host=DB_HOST, user=DB_USER, password=DB_PASS, database=DB_NAME
    )
