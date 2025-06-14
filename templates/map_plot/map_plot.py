from dash import Dash, dcc, html, callback, Input, Output

from dash_mantine_components import MantineProvider
import dash_mantine_components as dmc

from static.src.data.map_data_1 import data_plot_ce, data_table_ce

from static.src.plots.map_plot_1 import map_plot_ce, table_plot

fig_map   = map_plot_ce(data_plot_ce())
fig_table = table_plot(data_table_ce('Fortaleza'))

def map_plot_dash(appFlask):
    # Outras configs importantes
    configs = {'displaylogo': False, 'displayModeBar':False} # remove o logo do dash
    
    paper = dict(p="xs", shadow="xl", mt="md", withBorder=True)
    

    app = Dash(
        name="dashboardStatic", 
        title="BI da Sesa", 
        server = appFlask, 
        url_base_pathname='/home/map_plot/',
    )
    #-----------------------

    # ----------------------

    app.layout = MantineProvider([ 
        dmc.Grid([
            dmc.GridCol([
                dmc.Paper([
                    dcc.Graph(
                        id='map_plot_ce',
                        figure=fig_map,
                        config=configs
                    ),
                ], **paper)
            ], span=6),
            dmc.GridCol([
                dmc.Paper([
                    dcc.Graph(
                        id='table_plot_ce',
                        figure=fig_table,
                        config=configs
                    ),
                    dmc.Text("Selecione um município no mapa", id='texto',c="dimmed", style={'margin-top': '-20px','position':'absolute'})
                ], **paper)
            ], span=4)
        ], gutter="xs", align="stretch", justify='center')
    ])

    @app.callback(
        Output(component_id='table_plot_ce', component_property='figure'), 
        Input(component_id='map_plot_ce', component_property='hoverData'),
    )
    def update_graph(hoverData):
        if hoverData is None:
            return fig_table
        points = hoverData['points'][0]

        if points['z'] == 0:
            return fig_table
        
        return table_plot(data_table_ce(points['text']))
    
    return app.server