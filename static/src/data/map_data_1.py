
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



def data_plot_ce():
    query = '''
SELECT 
  cidades.nome AS nome_cidade,
  SUM(tratamentos.custo_total),
  COUNT(*)
FROM 
  cidades
INNER JOIN tratamentos ON 
  cidades.cidade_id = tratamentos.cidade_id 
GROUP BY nome_cidade;
'''
    conn.rollback()
    data = pd.read_sql_query(query, conn)
    data['nome_cidade'] = data['nome_cidade'].str.title()
    return data


def data_barplot11_ce(cidade='fortaleza'):
    cidade = cidade.lower()
    query = f'''
SELECT 
  enfermidades.nome AS nome_enfermidade,
  SUM(tratamentos.custo_total) AS custo_total
FROM 
  cidades
INNER JOIN tratamentos ON 
  cidades.cidade_id = tratamentos.cidade_id 
INNER JOIN enfermidades ON 
  tratamentos.enfermidade_id = enfermidades.enfermidade_id
WHERE LOWER(cidades.nome) = '{cidade}'
GROUP BY nome_enfermidade
ORDER BY custo_total DESC;
'''

    for i in range(3): conn.rollback()
    data = pd.read_sql_query(query, conn)
    data['sum_humanize'] = data['custo_total'].apply( lambda x: humanize.intword(x).replace('hundred', 'mil') if 'hundred' in humanize.intword(x) else humanize.intword(x)  )
    data['sum_humanize'] = data['sum_humanize'].str.replace("million", "milhão")
    return data


def data_barplot_ce(cidade='fortaleza'):
    cidade = cidade.lower()
    query = f'''
SELECT
  enfermidades.nome AS nome_enfermidade,
  enfermidades.gravidade AS gravidade,
  COUNT(*) AS quantidade
FROM
  cidades
INNER JOIN tratamentos ON
  cidades.cidade_id = tratamentos.cidade_id
INNER JOIN enfermidades ON
  tratamentos.enfermidade_id = enfermidades.enfermidade_id
WHERE LOWER(cidades.nome) = '{cidade}'
GROUP BY nome_enfermidade, gravidade
ORDER BY nome_enfermidade;
'''
    for i in range(3): conn.rollback()
    return pd.read_sql_query(query, conn)