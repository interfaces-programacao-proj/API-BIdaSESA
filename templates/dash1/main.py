
import plotly.graph_objects as go
import dash_mantine_components as dmc
from dash import Dash, dcc, html, _dash_renderer
from dash_mantine_components import MantineProvider






def dashboard1(appFlask):
    # Outras configs importantes
    configs = {'displaylogo': False, 'displayModeBar':False} # remove o logo do dash
    
    app = Dash(
        name="dashboardStatic", 
        title="Dashboard"    , 
        external_stylesheets=[dmc.styles.ALL], 
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
    configsCard        = dict(withBorder=True, shadow="sm", radius="md")
    configsCardSection = dict(withBorder=True, inheritPadding=True, py="xs")
    
    linha0 = dmc.Grid([
        dmc.GridCol([   
            dmc.Card([
                dmc.CardSection([
                    dmc.Text("titulo", size="sm")
                ], **configsCardSection),
                dmc.Text('valor', fw=500, size="lg")
            ], **configsCard)
        ], span=3),
    
        dmc.GridCol([   
            dmc.Card([
                dmc.CardSection([
                    dmc.Text("titulo", size="sm")
                ], **configsCardSection),
                dmc.Text('valor', fw=500, size="lg")
            ], **configsCard)
        ], span=3),
    ], gutter="xs", align="stretch", justify='center')
    
    ## Linha 1
    
    paper  = dict(p="xs", shadow="xl", mt="md", withBorder=True, style={'height':'100%', 'width':'100%'})
    
    linha1 = dmc.Grid([
        dmc.GridCol([
            dmc.Paper([
                dcc.Graph(figure=fig, config=configs)
            ], **paper)
        ], span=3),
        
        dmc.GridCol([
            dmc.Paper([
                dcc.Graph(figure=fig, config=configs)
            ], **paper)
        ], span=3),
        
        dmc.GridCol([
            dmc.Paper([
                dcc.Graph(figure=fig, config=configs)
            ], **paper)
        ], span=3),
    ], gutter="xs", align="stretch", justify='center')
    
    
    ## Linha 2
    paper  = dict(p="xs", shadow="xl", mt="md", withBorder=True, style={'height':'100%', 'width':'100%'})
    
    linha2 = dmc.Grid([
        dmc.GridCol([
            dmc.Paper([
                dcc.Graph(figure=fig, config=configs)
            ], **paper)
        ], span=3),
        
        dmc.GridCol([
            dmc.Paper([
                dcc.Graph(figure=fig, config=configs)
            ], **paper)
        ], span=3),
        
        dmc.GridCol([
            dmc.Paper([
                dcc.Graph(figure=fig, config=configs)
            ], **paper)
        ], span=3),
    ], gutter="xs", align="stretch", justify='center')
    
    ### --------------------------
    # Layout
    app.layout = MantineProvider([
        dmc.Stack([
            linha0,
            linha1,
            linha2
        ], gap="xs"),
    ])

    return app.server