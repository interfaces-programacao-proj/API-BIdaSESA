import plotly.graph_objects as go
import dash_mantine_components as dmc
from dash import Dash, dcc, html, _dash_renderer
from dash_mantine_components import MantineProvider

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


style = '''
@import url('https://fonts.googleapis.com/css2?family=Inter&display=swap');

* {
    background-color: #f2e8cf;
    font-family: 'Inter', sans-serif;
}
'''
def dashboard1(appFlask):
    # Outras configs importantes
    configs = {'displaylogo': False, 'displayModeBar':False} # remove o logo do dash
    
    app = Dash(
        name="dashboardStatic", 
        title="Dashboard", 
        server = appFlask, 
        url_base_pathname='/home/dash1/',
    )

    #Veja se essa config não foi atualizada
    _dash_renderer._set_react_version('18.2.0')

    # COLOQUE OS GRAFICOS ABAIXO
    fig = go.Figure()
    fig.update_layout(height=300)
    
    ## --------------------------
    
    ## Linha 0 - Coloque os cards
    paper0 = dict(p="xs", shadow="xl", mt="md", withBorder=True, style={'height':'100%', 'width':'100%'})
    
    col0 = dmc.Paper([
        dmc.Stack([
            dmc.MultiSelect(
                data = [
                    {'label': municipio, 'value': municipio} \
                        for municipio in municipios
                ],
                value = municipios[3:5],
                label="Municipios",
                size = 'sm'
            ),
            dmc.MultiSelect(
                data = [
                    {'label': enfermidade, 'value': enfermidade} \
                        for enfermidade in enfermidades
                ],
                value = enfermidades[0:2],
                label="Enfermidades",
                size = 'sm'
            ),
            dmc.DateInput(
                label="Data Inicial",
                value='2025-01-01'
            ),
            dmc.DateInput(
                label="Data Final",
                value='2022-01-01'
            ),
        ]),
    ],**paper0)	
    

    # Coluna 1
    paper = dict(p="xs", shadow="xl", mt="md", withBorder=True, style={'height':'100%', 'width':'100%'})
    
    col1 = dmc.Grid([
        dmc.GridCol([
            dmc.Paper([
                dcc.Graph(figure=fig, config=configs)
            ], **paper)
        ], span=4),
        
        dmc.GridCol([
            dmc.Paper([
                dcc.Graph(figure=fig, config=configs)
            ], **paper)
        ], span=4),
        
        dmc.GridCol([
            dmc.Paper([
                dcc.Graph(figure=fig, config=configs)
            ], **paper)
        ], span=4),
                dmc.GridCol([
            dmc.Paper([
                dcc.Graph(figure=fig, config=configs)
            ], **paper)
        ], span=4),
        
        dmc.GridCol([
            dmc.Paper([
                dcc.Graph(figure=fig, config=configs)
            ], **paper)
        ], span=4),
        
        dmc.GridCol([
            dmc.Paper([
                dcc.Graph(figure=fig, config=configs)
            ], **paper)
        ], span=4),
    ], gutter="xs", align="stretch", justify='center')
    
    
    ### --------------------------
    # Layout
    app.layout = html.Div(
        style={'margin': '10px'},
        children=[
            MantineProvider(
                theme={
                    "colorScheme": "light",
                    "primaryColor": "blue",
                    "components": {
                        "Paper": {
                            "styles": {"root": {"backgroundColor": "#ffffff"}},
                        },
                        "Card": {
                            "styles": {"root": {"backgroundColor": "#ffffff"}},
                        }
                    }
                },
                children=[
                    dmc.Grid(
                        [
                            dmc.GridCol(col0, span=2.8),
                            dmc.GridCol(col1, span=9),
                        ],
                        gutter="xs",
                        align="stretch",
                        justify='center',
                        style={'width':'100%'}
                    )
                ],

            )
        ]
    )

    return app.server