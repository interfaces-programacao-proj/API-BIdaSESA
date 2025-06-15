import json 
import psycopg2
from   sqlalchemy import create_engine
import pandas as pd
with open('backend/key.txt', 'r') as f:
    DATABASE_URL = f.read()

engine = create_engine(DATABASE_URL)
conn = engine.connect()
conn.rollback()


municipios = [
    "Fortaleza", "Caucaia", 
    "Juazeiro do Norte", "Maracanaú", 
    "Sobral", "Crato", "Itapipoca",
      "Maranguape", "Quixadá", "Aquiraz"
]
enfermidades = ['Dengue',
                'Chikungunya',
                'Zika',
                'Leptospirose',
                'Hepatite A',
                'Hepatite B',
                'Tuberculose',
                'Malária',
                'Febre Amarela',
                'Covid-19',
                'HIV/AIDS',
                'Hanseníase'
]

def data_barplot_1(data_inicio='2023-06-12', cidade=municipios, enfermidade=enfermidades):
    array_literal = "ARRAY[" + ",".join(f"'{s}'" for s in cidade) + "]::text[]"
    array_literal_enfermidades = "ARRAY[" + ",".join(f"'{s}'" for s in enfermidade) + "]::text[]"
    query = f'''
SELECT 
    cidades.nome,
    COUNT(*) AS incidencias
FROM 
    cidades 
INNER JOIN tratamentos ON 
    tratamentos.cidade_id = cidades.cidade_id
INNER JOIN enfermidades ON
    tratamentos.enfermidade_id = enfermidades.enfermidade_id
WHERE
    tratamentos.data_inicio >= '{data_inicio}' 
    AND cidades.nome      = ANY({array_literal})
    AND enfermidades.nome = ANY({array_literal_enfermidades})
GROUP BY 
    cidades.nome
ORDER BY 
    COUNT(*) DESC;
'''
    for i in range(3): conn.rollback()
    return pd.read_sql_query(query, conn)


#---------------- PIZZA -----------------
def data_pieplot_1(data_inicio='2023-06-12', cidade=municipios, enfermidade=enfermidades):
    array_literal = "ARRAY[" + ",".join(f"'{s}'" for s in cidade) + "]::text[]"
    array_literal_enfermidades = "ARRAY[" + ",".join(f"'{s}'" for s in enfermidade) + "]::text[]"

    query = f'''
SELECT 
    pacientes.sexo,
    COUNT(*)
FROM 
    pacientes
INNER JOIN tratamentos ON
    tratamentos.paciente_id = pacientes.paciente_id
INNER JOIN cidades ON 
    tratamentos.cidade_id = cidades.cidade_id
INNER JOIN enfermidades ON
    tratamentos.enfermidade_id = enfermidades.enfermidade_id
WHERE
    tratamentos.data_inicio >= '{data_inicio}' 
    AND cidades.nome      = ANY({array_literal})
    AND enfermidades.nome = ANY({array_literal_enfermidades})
GROUP BY pacientes.sexo
'''
    for i in range(3): conn.rollback()
    
    return pd.read_sql_query(query, conn)