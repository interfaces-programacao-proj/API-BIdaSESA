
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


def data_table_ce(cidade):
    query = f'''
SELECT 
  enfermidades.nome AS nome_enfermidade,
  COUNT(*),
  SUM(tratamentos.custo_total),
  RANK() OVER ( ORDER BY SUM(tratamentos.custo_total) DESC) AS rank_custo_total,
  RANK() OVER ( ORDER BY COUNT(*) DESC) AS rank_count

FROM 
  cidades
INNER JOIN tratamentos ON 
  cidades.cidade_id = tratamentos.cidade_id 
INNER JOIN enfermidades ON 
  tratamentos.enfermidade_id = enfermidades.enfermidade_id
WHERE LOWER(cidades.nome) = '{cidade.lower()}'
GROUP BY nome_enfermidade
ORDER BY nome_enfermidade;
'''

    conn.rollback()
    data = pd.read_sql_query(query, conn)
    data['sum'] = data['sum'].apply( lambda x: humanize.intword(x).replace('hundred', 'mil') if 'hundred' in humanize.intword(x) else humanize.intword(x)  )
    data['sum'] = data['sum'].str.replace("million", "milhão")
    return data