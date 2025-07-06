from   sqlalchemy import create_engine
import psycopg2 
import pandas as pd

with open('backend/key.txt', 'r') as f:
    DATABASE_URL = f.read()



def get_enfermidades():
    engine = create_engine(DATABASE_URL)
    conn = engine.connect()
    result = conn.execute("SELECT * FROM enfermidades").fetchall()
    conn.close()
    # to pandas
    result = pd.DataFrame(result, columns=['id', 'enfermidade', 'descricao', 'gravidade', 'sintomas'])
    return result
