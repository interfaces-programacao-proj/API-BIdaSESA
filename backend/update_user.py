from   sqlalchemy import create_engine, text
import psycopg2 
import pandas as pd


with open('backend/key.txt', 'r') as f:
    DATABASE_URL = f.read()


def update_user(email, username, password):
    engine = create_engine(DATABASE_URL)
    conn = engine.connect()
    conn.rollback()
    # Evita SQL Injection e é executável
    query = text("UPDATE user_system SET nome = :username, password = :password WHERE email = :email")

    conn.execute(query, {"username": username, "password": password, "email": email})
    conn.commit()

    return True