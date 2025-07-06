from   sqlalchemy import create_engine
import psycopg2 
import pandas as pd

with open('backend/key.txt', 'r') as f:
    DATABASE_URL = f.read()



def get_enfermidades():
    engine = create_engine(DATABASE_URL)
    conn = engine.connect()
    conn.rollback()
    data = pd.read_sql_query('SELECT * FROM enfermidades', conn)
    data.rename(columns={'nome':'enfermidade'}, inplace=True)
    return data
