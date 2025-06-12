from dash_mantine_components import MantineProvider
import dash_mantine_components as dmc
from dash import Dash, dcc, html, _dash_renderer



def descricao_page(appFlask):
    app = Dash(
        name="dashboardStatic", 
        title="Dashboard", 
        server = appFlask, 
        url_base_pathname='/home/descricao_page/',
    )
    # ----------------------
    _dash_renderer._set_react_version('18.2.0')

    app.layout = MantineProvider([
        dmc.Title('oi'),
    ])
    return app.server