from dash import Dash, dcc, html, callback, Input, Output, no_update, _dash_renderer
from   dash_mantine_components import MantineProvider
import dash_mantine_components as dmc

from static.src.data.map_data_1  import data_plot_ce, data_barplot11_ce, data_barplot_ce

from static.src.plots.map_plot_1 import map_plot_ce, barplot_ce, barplot11_ce, pie_hoverlabel


#----------------------- PLOTS
fig_map   = map_plot_ce(data_plot_ce())

fig_table = barplot11_ce(data_barplot11_ce('fortaleza'))

fig_bar   = barplot_ce(data_barplot_ce('fortaleza'))
#-----------------------


def map_plot_dash(appFlask):
    lista = ['fortaleza']
    # Outras configs importantes
    configs = {'displaylogo': False, 'displayModeBar':False} # remove o logo do dash
    
    paper = dict(p="xs", shadow="xl", mt="md", withBorder=True, bg='#eae0d5')
    

    app = Dash( name="dashboardStatic",  title="BI da Sesa", server = appFlask,  url_base_pathname='/home/map_plot/' )

    #Veja se essa config nao foi atualizada
    #_dash_renderer._set_react_version('18.2.0')

    #-----------------------
    app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <style>
            body {
                background-color: #c6ac8f !important;
                margin: 0;
                padding: 0;
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''
    # ----------------------
    linha0 = dmc.Grid([
                dmc.GridCol([
                    dmc.Paper([
                        dcc.Graph( id='map_plot_ce', figure=fig_map, config=configs ),
                        dmc.Text("Selecione um município no mapa",  id='texto',c="dimmed",  
                                 style={'margin-top': '-20px','position':'absolute'}
                        )
                    ], **paper)
                ], span=6),
                dmc.GridCol([
                    dmc.Paper([
                        dcc.Graph( id='table_plot_ce', figure=fig_table, config=configs ),
                    ], **paper)
                ], span=4),
            ], gutter="xs", align="stretch", justify='center')
    
    linha1 = dmc.Paper([
                dcc.Graph( id='barplot_ce', figure=fig_bar, config=configs, clear_on_unhover=True ),
                dcc.Tooltip(id="barplot-tooltip", direction="top", background_color='#eae0d5'),
            ], **paper, style={'width':'35%'} )
    
    app.layout = MantineProvider([ 
        dmc.Container([
            linha0,
            dmc.Center([linha1])
        ], fluid=True)

    ])




    #--------------------------------------------------------
    @app.callback(
        Output(component_id='table_plot_ce', component_property='figure'), 
        Input(component_id='map_plot_ce', component_property='hoverData'),
    )
    def update_graph(hoverData):
        if hoverData is None: return fig_table
        
        points = hoverData['points'][0]
        
        if points['z'] == 0: return no_update

        lista.append(points['text'])
      
        return barplot11_ce(data_barplot11_ce(points['text']), points['text'])
    
    
    #--------------------------------------------------------
    @app.callback(
        Output(component_id='barplot_ce', component_property='figure'), 
        Input(component_id='map_plot_ce', component_property='hoverData'),
    )
    def update_graph2(hoverData):
        if hoverData is None: return fig_bar
        
        points = hoverData['points'][0]

        if points['z'] == 0: return no_update
        return barplot_ce(data_barplot_ce(points['text']), points['text'])
    


    #--------------------------------------------------------
    @app.callback(
        Output("barplot-tooltip", "show"),
        Output("barplot-tooltip", "bbox"),
        Output("barplot-tooltip", "children"),
        Input("barplot_ce", "hoverData"),
    )
    def hover_callback(hoverData):
        if hoverData is None: return False, no_update, no_update
        
        points   = hoverData['points'][0]
        bbox     = points["bbox"]
        children = [dcc.Graph( figure=pie_hoverlabel(data_barplot_ce(lista[-1]), points['y'], lista[-1]) , config=configs)]
        return True, bbox, children


    return app.server