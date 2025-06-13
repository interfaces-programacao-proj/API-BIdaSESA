import pandas as pd

from dash_mantine_components import ListItem, Text, Title, Paper, Stack, List, Space
def tratamento_enfermidade(enfermidades):
    text  = []
    nome_enfermidades = enfermidades['enfermidade'].unique()

    for nome in nome_enfermidades:
        lista  = []
        subset = enfermidades[enfermidades['enfermidade'] == nome]
        lista.append(Title(f'{nome}', order=3))
        
        lista_items = []
        for tupla in subset.iterrows():
            lista_items.append(
                ListItem([
                    Text(f'{tupla[1]['gravidade']} : ', fw=700, span=True),
                    Text(f'{tupla[1]['sintomas']}', span=True)
                ])
            )
        lista.append(List(children=lista_items))
        lista.append(
            Text(f'Descrição: {subset['descricao'].values[0]}')
        )
        text.append(Paper(children=lista, p="xs", shadow="xl", mt="md", withBorder=True, style={'height':'100%', 'width':'60%'}))
    text.insert(0, Title('Enfermidades', order=2))
    text.insert(0, Space(h=10))

    return Stack(text, align="center", gap=1)