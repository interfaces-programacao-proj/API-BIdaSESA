from dash_mantine_components import MantineProvider
import dash_mantine_components as dmc
from dash import Dash, dcc, html, _dash_renderer


from backend.descricao_enfermidades import get_enfermidades
from static.code.tratamento_enfermidade import tratamento_enfermidade


def descricao_page(appFlask):
    enfermidades = get_enfermidades()
    text = tratamento_enfermidade(enfermidades)
    app = Dash(
        name="dashboardStatic", 
        title="BI da Sesa", 
        server = appFlask, 
        url_base_pathname='/home/descricao_page/',
    )
    # ----------------------
    _dash_renderer._set_react_version('18.2.0')


    app.layout = MantineProvider([
        html.Div([
            text    
        ], style={
            'background-color': '#c6ac8f',
        })
    ], theme={
        "fontFamily": "'Inter', sans-serif",
    })
    return app.server