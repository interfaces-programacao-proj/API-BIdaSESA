from   sqlalchemy import create_engine
import psycopg2 
import pandas as pd

with open('backend/key.txt', 'r') as f:
    DATABASE_URL = f.read()



def get_enfermidades():
    conn = psycopg2.connect(DATABASE_URL)
    query = "SELECT * FROM enfermidades"
    cursor = conn.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    # to pandas
    result = pd.DataFrame(result, columns=['id', 'enfermidade', 'descricao', 'gravidade', 'sintomas'])
    return result