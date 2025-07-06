from   sqlalchemy import create_engine
import psycopg2 
import pandas as pd


with open('backend/key.txt', 'r') as f:
    DATABASE_URL = f.read()

def user_exists(username, email, password, net=False):
    conn = psycopg2.connect(DATABASE_URL)

    # verificando a existencia
    email = '' if net else "AND email = '"+email+"'"
    query = f'''
SELECT
    *
FROM 
    user_system 
WHERE
    nome = '{username}' AND password = '{password}'
'''
    
    cursor = conn.cursor()
    conn.rollback()
    cursor.execute(query)
    result = cursor.fetchall()
    print(result)
    cursor.close()
    conn.close()

    if len(result) > 0:
        if net: return True
        return False
    else:
        return True


def create_user(email, username, password):
    if not user_exists(username, email, password):
        return False
    
    conn = psycopg2.connect(DATABASE_URL)
    conn.rollback()

    
    query = f"INSERT INTO user_system (nome, email , password) VALUES ('{username}', '{email}', '{password}')"
    conn.rollback()
    cursor = conn.cursor()
    cursor.execute(query, (email, username, password))
    conn.commit()
    cursor.close()
    conn.close()
    return True


def return_json_data(username, password):
    query = f'''
SELECT
    *
FROM 
    user_system 
WHERE
    nome = '{username}' AND password = '{password}'
LIMIT 1
'''
    conn = psycopg2.connect(DATABASE_URL)
    conn.rollback()
    data = pd.read_sql_query(query, conn)
    print(data)
    return data.to_json(orient='records')
