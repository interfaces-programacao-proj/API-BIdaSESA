from   sqlalchemy import create_engine
import psycopg2 
import pandas as pd


with open('backend/key.txt', 'r') as f:
    DATABASE_URL = f.read()


def user_exists_login(email, password):
    engine = create_engine(DATABASE_URL)
    conn = engine.connect()
    conn.rollback()

    query = f'''
SELECT
    *
FROM
    user_system
WHERE
    email = '{email}' AND password = '{password}'
'''

    result = pd.read_sql_query(query, conn)

    if len(result) > 0:
        return True
    else:
        return False
    
def user_exists(username, email, password, net=False):
    engine = create_engine(DATABASE_URL)
    conn = engine.connect()
    conn.rollback()
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
    
    result = pd.read_sql_query(query, conn)

    if len(result) > 0:
        if net: return True
        return False
    else:
        return True


def create_user(email, username, password):
    if not user_exists(username, email, password):
        return False
    
    engine = create_engine(DATABASE_URL)
    conn = engine.connect()
    conn.rollback()
    conn.execute(f"INSERT INTO user_system (nome, email , password) VALUES ('{username}', '{email}', '{password}')")
    conn.commit()
    return True


def return_json_data(username):
    query = f'''
SELECT
    *
FROM 
    user_system 
WHERE
    email = '{username}'
LIMIT 1
'''
    engine = create_engine(DATABASE_URL)
    with engine.connect() as connection:
        transaction = connection.begin()
        try:
            data = pd.read_sql_query(query, connection)
            transaction.commit()
        except:
            transaction.rollback()
            raise
    
    return data.to_dict('dict')
