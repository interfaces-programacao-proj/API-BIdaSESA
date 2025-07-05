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
    data['total_incidencias'] = data['total_incidencias'].apply(lambda x: humanize.intword(str(x)).replace('thousand', 'mil').replace('million','Milhão'))
    try:
        return data['total_incidencias'].values[0]
    except:
        return 'Nenhum'
    

#-------------------------
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
    


#---------------- BAR PLOT ----------------
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


#---------------- bar plot -----------------
## Faixa etaria x custo
def data_barplot_3(data_inicio='2023-06-12', data_fim='2025-06-11', cidade=municipios, enfermidade=enfermidades):
    array_literal = "ARRAY[" + ",".join(f"'{s}'" for s in cidade) + "]::text[]"
    array_literal_enfermidades = "ARRAY[" + ",".join(f"'{s}'" for s in enfermidade) + "]::text[]"

    query = f'''
WITH tabela_idade AS (
  SELECT 
    EXTRACT( YEAR FROM CURRENT_DATE)  - EXTRACT( YEAR FROM data_nascimento) AS idade,
    paciente_id
  FROM 
    pacientes
),
faixa_etaria AS (
  SELECT CASE
    WHEN idade <= 1                THEN 'Bebe'
    WHEN idade > 1 AND idade <= 12 THEN 'Criança'
    WHEN idade > 12 AND idade <= 18 THEN 'Adolescente'
    WHEN idade > 18 AND idade <=25  THEN 'Jovem'
    WHEN idade > 25 AND idade <=60  THEN 'Adulto'
    WHEN idade > 60 AND idade <=75  THEN 'Idoso J'
    WHEN idade > 75 THEN 'Idoso velho'
    else 'idoso'
  END AS faixa,
  paciente_id
  FROM tabela_idade
)
SELECT 
  faixa,
  SUM(tratamentos.custo_total) AS custo_total
FROM 
  faixa_etaria
INNER JOIN tratamentos ON  
  tratamentos.paciente_id = faixa_etaria.paciente_id
INNER JOIN cidades ON 
  tratamentos.cidade_id = cidades.cidade_id
INNER JOIN enfermidades ON
  tratamentos.enfermidade_id = enfermidades.enfermidade_id
WHERE 
    tratamentos.data_inicio BETWEEN '{data_inicio}' AND '{data_fim}'
    AND enfermidades.nome = ANY({array_literal_enfermidades}) 
    AND cidades.nome      = ANY({array_literal})
GROUP BY faixa
ORDER BY custo_total DESC;
'''
    for i in range(3): conn.rollback()
    data = pd.read_sql_query(query, conn)
    data['custo_total_cat'] = data["custo_total"].apply(lambda x: humanize.intword(x).replace('thousand', 'mil').replace('billion','bilhão').replace('million', 'milhão'))
    return data



# ---------------- bar plot -----------------
## Faixa etaria x tempo médio
def data_barplot_4(data_inicio='2023-06-12', data_fim='2025-06-11', cidade=municipios, enfermidade=enfermidades):
    array_literal = "ARRAY[" + ",".join(f"'{s}'" for s in cidade) + "]::text[]"
    array_literal_enfermidades = "ARRAY[" + ",".join(f"'{s}'" for s in enfermidade) + "]::text[]"

    query = f'''
WITH tabela_idade AS (
  SELECT 
    EXTRACT( YEAR FROM CURRENT_DATE)  - EXTRACT( YEAR FROM data_nascimento) AS idade,
    paciente_id
  FROM 
    pacientes
),
faixa_etaria AS (
  SELECT CASE
    WHEN idade <= 1                THEN 'Bebe'
    WHEN idade > 1 AND idade <= 12 THEN 'Criança'
    WHEN idade > 12 AND idade <= 18 THEN 'Adolescente'
    WHEN idade > 18 AND idade <=25  THEN 'Jovem'
    WHEN idade > 25 AND idade <=60  THEN 'Adulto'
    WHEN idade > 60 AND idade <=75  THEN 'Idoso J'
    WHEN idade > 75 THEN 'Idoso velho'
    else 'idoso'
  END AS faixa,
  paciente_id
  FROM tabela_idade
)
SELECT 
  faixa,
  AVG(tratamentos.data_fim - tratamentos.data_inicio) AS tempo_medio
FROM 
  faixa_etaria
INNER JOIN tratamentos ON  
  tratamentos.paciente_id = faixa_etaria.paciente_id
INNER JOIN cidades ON 
    tratamentos.cidade_id = cidades.cidade_id
INNER JOIN enfermidades ON
    tratamentos.enfermidade_id = enfermidades.enfermidade_id
WHERE
    tratamentos.data_inicio BETWEEN '{data_inicio}' AND '{data_fim}' 
    AND cidades.nome      = ANY({array_literal})
    AND enfermidades.nome = ANY({array_literal_enfermidades})
GROUP BY faixa
ORDER BY tempo_medio DESC;
'''
    for i in range(3): conn.rollback()
    data = pd.read_sql_query(query, conn)
    data['tempo_medio_cat'] = data['tempo_medio'].apply(lambda x: str(round(x,2))+ ' dias' )
    return data


#---------------- lineplot -----------------

def data_lineplot_1( data_inicio='2023-06-12', data_fim='2025-06-11', cidade=municipios, enfermidade=enfermidades):
    array_literal = "ARRAY[" + ",".join(f"'{s}'" for s in cidade) + "]::text[]"
    array_literal_enfermidades = "ARRAY[" + ",".join(f"'{s}'" for s in enfermidade) + "]::text[]"
    query = f'''
SELECT
  tratamentos.data_inicio,
  COUNT(*)
FROM 
  tratamentos
INNER JOIN cidades ON 
    tratamentos.cidade_id = cidades.cidade_id
INNER JOIN enfermidades ON
    tratamentos.enfermidade_id = enfermidades.enfermidade_id
WHERE
    tratamentos.data_inicio BETWEEN '{data_inicio}' AND '{data_fim}' 
    AND cidades.nome      = ANY({array_literal})
    AND enfermidades.nome = ANY({array_literal_enfermidades})
GROUP BY tratamentos.data_inicio;
'''
    for i in range(2):conn.rollback()

    return pd.read_sql_query(query, conn)



def data_barplot_5( data_inicio='2023-06-12', data_fim='2025-06-11', cidade=municipios, enfermidade=enfermidades):
    array_literal = "ARRAY[" + ",".join(f"'{s}'" for s in cidade) + "]::text[]"
    array_literal_enfermidades = "ARRAY[" + ",".join(f"'{s}'" for s in enfermidade) + "]::text[]"
    query = f'''
WITH tabela_idade AS (
  SELECT 
    EXTRACT( YEAR FROM CURRENT_DATE)  - EXTRACT( YEAR FROM data_nascimento) AS idade,
    paciente_id
  FROM 
    pacientes
),
faixa_etaria AS (
  SELECT CASE
    WHEN idade <= 1                THEN 'Bebe'
    WHEN idade > 1 AND idade <= 12 THEN 'Criança'
    WHEN idade > 12 AND idade <= 18 THEN 'Adolescente'
    WHEN idade > 18 AND idade <=25  THEN 'Jovem'
    WHEN idade > 25 AND idade <=60  THEN 'Adulto'
    WHEN idade > 60 AND idade <=75  THEN 'Idoso J'
    WHEN idade > 75 THEN 'Idoso velho'
    else 'idoso'
  END AS faixa,
  paciente_id
  FROM tabela_idade
)
SELECT 
  faixa,
  enfermidades.gravidade,
  count(*) AS casos_total
FROM 
  faixa_etaria
INNER JOIN tratamentos ON  
  tratamentos.paciente_id = faixa_etaria.paciente_id
INNER JOIN enfermidades ON  
  tratamentos.enfermidade_id = enfermidades.enfermidade_id
INNER JOIN cidades ON 
    tratamentos.cidade_id = cidades.cidade_id
WHERE
    tratamentos.data_inicio BETWEEN '{data_inicio}' AND '{data_fim}' 
    AND cidades.nome      = ANY({array_literal})
    AND enfermidades.nome = ANY({array_literal_enfermidades})
GROUP BY faixa, enfermidades.gravidade
ORDER BY faixa DESC;
''' 
    for i in range(2): conn.rollback()

    return pd.read_sql_query(query, conn)



#---------------- plot -----------------

def data_barplot_6( data_inicio='2023-06-12', data_fim='2025-06-11', cidade=municipios, enfermidade=enfermidades):
    array_literal = "ARRAY[" + ",".join(f"'{s}'" for s in cidade) + "]::text[]"
    array_literal_enfermidades = "ARRAY[" + ",".join(f"'{s}'" for s in enfermidade) + "]::text[]"
    query = f'''
WITH tabela_idade AS (
  SELECT 
    EXTRACT( YEAR FROM CURRENT_DATE)  - EXTRACT( YEAR FROM data_nascimento) AS idade,
    paciente_id
  FROM 
    pacientes
),
faixa_etaria AS (
  SELECT CASE
    WHEN idade <= 1                THEN 'Bebe'
    WHEN idade > 1 AND idade <= 12 THEN 'Criança'
    WHEN idade > 12 AND idade <= 18 THEN 'Adolescente'
    WHEN idade > 18 AND idade <=25  THEN 'Jovem'
    WHEN idade > 25 AND idade <=60  THEN 'Adulto'
    WHEN idade > 60 AND idade <=75  THEN 'Idoso J'
    WHEN idade > 75 THEN 'Idoso velho'
    else 'idoso'
  END AS faixa,
  paciente_id
  FROM tabela_idade
)
SELECT 
  faixa,
  enfermidades.gravidade,
  AVG(tratamentos.custo_total) AS custo_médio
FROM 
  faixa_etaria
INNER JOIN tratamentos ON  
  tratamentos.paciente_id = faixa_etaria.paciente_id
INNER JOIN enfermidades ON  
  tratamentos.enfermidade_id = enfermidades.enfermidade_id
INNER JOIN cidades ON 
    tratamentos.cidade_id = cidades.cidade_id
WHERE
    tratamentos.data_inicio BETWEEN '{data_inicio}' AND '{data_fim}' 
    AND cidades.nome      = ANY({array_literal})
    AND enfermidades.nome = ANY({array_literal_enfermidades})
GROUP BY faixa, enfermidades.gravidade
ORDER BY faixa DESC;
'''
    for i in range(2):conn.rollback()

    return pd.read_sql_query(query, conn)

