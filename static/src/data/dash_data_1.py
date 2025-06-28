import json 
import psycopg2
from   sqlalchemy import create_engine
import pandas as pd


import humanize
# Para usar em português (necessário instalar o pacote de linguagem)
humanize.activate('pt_BR')

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

# Cards 
def data_card_1(data_inicio='2023-06-12', data_fim='2025-10-11',cidade=municipios, enfermidade=enfermidades):
    array_literal = "ARRAY[" + ",".join(f"'{s}'" for s in cidade) + "]::text[]"
    array_literal_enfermidades = "ARRAY[" + ",".join(f"'{s}'" for s in enfermidade) + "]::text[]"
    query = f'''
SELECT 
    COUNT(*) AS total_incidencias
FROM 
    tratamentos
INNER JOIN cidades ON 
    tratamentos.cidade_id = cidades.cidade_id
INNER JOIN enfermidades ON
    tratamentos.enfermidade_id = enfermidades.enfermidade_id
WHERE
    tratamentos.data_inicio between '{data_inicio}' AND '{data_fim}' 
    AND cidades.nome      = ANY({array_literal})
    AND enfermidades.nome = ANY({array_literal_enfermidades})
'''
    for i in range(3): conn.rollback()
    data = pd.read_sql_query(query, conn)
    data['total_incidencias'] = data['total_incidencias'].apply(lambda x: humanize.intword(str(x)).replace('thousand', 'mil'))
    try:
        return data['total_incidencias'].values[0]
    except:
        return 'Nenhum'
    

def data_card_2(data_inicio='2023-06-12', data_fim='2025-10-11',cidade=municipios, enfermidade=enfermidades):
    array_literal = "ARRAY[" + ",".join(f"'{s}'" for s in cidade) + "]::text[]"
    array_literal_enfermidades = "ARRAY[" + ",".join(f"'{s}'" for s in enfermidade) + "]::text[]"
    query = f'''
SELECT 
    sum(tratamentos.custo_total) AS custo_total
FROM 
    tratamentos
INNER JOIN cidades ON 
    tratamentos.cidade_id = cidades.cidade_id
INNER JOIN enfermidades ON
    tratamentos.enfermidade_id = enfermidades.enfermidade_id
WHERE
    tratamentos.data_inicio between '{data_inicio}' AND '{data_fim}' 
    AND cidades.nome      = ANY({array_literal})
    AND enfermidades.nome = ANY({array_literal_enfermidades})
'''
    for i in range(3): conn.rollback()
    data = pd.read_sql_query(query, conn)
    data['custo_total'] = data['custo_total'].apply(lambda x: humanize.intword(x).replace('hundred', 'mil').replace('thousand', 'milhão').replace('billion', 'bilhão'))
    try:
        return data['custo_total'].values[0]
    except:
        return 'Nenhum'
    


def data_barplot_1(data_inicio='2023-06-12', data_fim='2025-10-11',cidade=municipios, enfermidade=enfermidades):
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
    tratamentos.data_inicio between '{data_inicio}' AND '{data_fim}' 
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
def data_pieplot_1(data_inicio='2023-06-12', data_fim='2025-10-11',cidade=municipios, enfermidade=enfermidades):
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
    tratamentos.data_inicio between '{data_inicio}' AND '{data_fim}' 
    AND cidades.nome      = ANY({array_literal})
    AND enfermidades.nome = ANY({array_literal_enfermidades})
GROUP BY pacientes.sexo
'''
    for i in range(3): conn.rollback()
    
    return pd.read_sql_query(query, conn)