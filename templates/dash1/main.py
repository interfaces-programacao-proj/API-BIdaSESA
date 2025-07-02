import plotly.graph_objects as go
import dash_mantine_components as dmc
from dash import Dash, dcc, html, _dash_renderer, Input, Output, callback, clientside_callback
from dash_mantine_components import MantineProvider



from static.src.plots.dash_plot_1 import (
    barplot_1,
    pieplot_1,
    barplot_3,
    barplot_4
)
from static.src.data.dash_data_1 import (
    data_barplot_1,
    data_pieplot_1,
    data_card_1,
    data_card_2,
    data_barplot_3,
    data_barplot_4
)

municipios = [
    "Fortaleza", "Caucaia", 
    "Juazeiro do Norte", "Maracanaú", 
    "Sobral", "Crato", "Itapipoca",
      "Maranguape", "Quixadá", "Aquiraz"
]
enfermidades = ['Dengue', 'Chikungunya', 'Zika', 'Leptospirose', 'Hepatite A', 'Hepatite B', 'Tuberculose',
                'Malária', 'Febre Amarela', 'Covid-19', 'HIV/AIDS', 'Hanseníase'
]

# ---------------------------------Cards---------------------------------

cards_1 = data_card_1()
cards_2 = data_card_2()

# ---------------------------------PLOTS---------------------------------
fig_1  = barplot_1(data_barplot_1())

fig_pie_1 = pieplot_1(data_pieplot_1())

fig_bar_3 = barplot_3(data_barplot_3())

fig_bar_4 = barplot_4(data_barplot_4())


# ---------------------------------DASHBOARD------------------------------
def dashboard1(appFlask):
    # Outras configs importantes
    configs = {'displaylogo': False, 'displayModeBar':False} # remove o logo do dash
    
    app = Dash( name="dashboardStatic", title="Dashboard", server = appFlask, url_base_pathname='/home/dash1/')

    #Veja se essa config não foi atualizada
    #_dash_renderer._set_react_version('18.2.0')

    # COLOQUE OS GRAFICOS ABAIXO
    fig = go.Figure()
    fig.update_layout(height=300)
    
    ## --------------------------
    app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter&display=swap');
            body {
                background-color: #c6ac8f !important;
                margin: 0;
                padding: 0;
                font-family: 'Inter', sans-serif;
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
    ## Linha 0 - Coloque os cards
    paper0 = dict(p="xs", shadow="xl", mt="md", withBorder=True, bg='#eae0d5')
    
    col0 = dmc.Paper([
        dmc.Stack([
            dmc.MultiSelect(
                data = [
                    {'label': municipio, 'value': municipio} \
                        for municipio in municipios
                ],
                value = municipios, label="Municipios", size = 'sm', id='municipios-select'
            ),
            dmc.MultiSelect(
                data = [
                    {'label': enfermidade, 'value': enfermidade} \
                        for enfermidade in enfermidades
                ],
                value = enfermidades, label="Enfermidades", size = 'sm', id='enfermidades-select'
            ),
            dmc.DateInput( label="Inicial", value='2023-06-12', id='start-date' ),
            dmc.DateInput( label="Final"  , value='2025-10-11', id='end-date' ),
        ]),
    ],**paper0)	

    # Cards
    cards1_ = dmc.Card([
            dmc.CardSection([
                dmc.Title("Casos totais", order=4),
            ], 
            withBorder    =True, 
            inheritPadding=True, 
            py="xs" ,
            style={'borderColor': '#1b263b'}
        ),
        dmc.Title(cards_1, id='casos_totais', order=5),
    ],
    mt="md",
    shadow="xl",
    withBorder=True, 
    w=300, 
    bg='#eae0d5' 
    )

    cards2_ = dmc.Card([
            dmc.CardSection([
                dmc.Title("Custo total", order=4),
            ], 
            withBorder    =True, 
            inheritPadding=True, 
            py="xs" ,
            style={'borderColor': '#1b263b'}
        ),
        dmc.Title(cards_2, id='custo_total', order=5),
    ],
    mt="md",
    shadow="xl",
    withBorder=True, 
    w=300, 
    bg='#eae0d5' 
    )         

    # Coluna 1
    paper = dict(p="xs", shadow="xl", mt="md", withBorder=True, bg='#eae0d5')
    
    col1 = dmc.Grid([
        dmc.GridCol([
            dmc.Grid([
                dmc.GridCol([ cards1_ ], span=2.8),
                dmc.GridCol([ cards2_ ], span=2.8),
            ],  gutter="xs", align="stretch", justify='center')        
        ]),
        
        dmc.GridCol([
            dmc.Paper([
                dcc.Graph(figure=fig_1, config=configs, id='grafico1')
            ], **paper)
        ], span=4),
        
        dmc.GridCol([
            dmc.Paper([
                dcc.Graph(figure=fig_bar_3, id='grafico_bar_3',config=configs)
            ], **paper)
        ], span=4),
        
        dmc.GridCol([
            dmc.Paper([
                dcc.Graph(figure=fig_bar_4, id='grafico_bar_4',config=configs)
            ], **paper)

        ], span=4),

        dmc.GridCol([
            dmc.Paper([
                dcc.Graph(figure=fig_pie_1, config=configs, id='grafico_pie_1')
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
    ], gutter=6, align="stretch", justify='center' )
    


    # Cards
    @app.callback(
        Output('casos_totais', 'children'),
        Output('custo_total', 'children'),
        Input('municipios-select', 'value'),
        Input('enfermidades-select', 'value'),
        Input('start-date', 'value'),
        Input('end-date', 'value'),
    )
    def update_cards(selected_municipios, selected_enfermidades, start_date, end_date):
        cards_1 = data_card_1(data_inicio=start_date, data_fim=end_date, cidade=selected_municipios, enfermidade=selected_enfermidades)
        cards_2 = data_card_2(data_inicio=start_date, data_fim=end_date, cidade=selected_municipios, enfermidade=selected_enfermidades)
        return cards_1, cards_2

    
    #-----------------------------------------
    @app.callback(
        Output('grafico_pie_1', 'figure'),
        Input('municipios-select', 'value'),
        Input('enfermidades-select', 'value'),
        Input('start-date', 'value'),
        Input('end-date', 'value'),
        
    )
    def update_graph(selected_municipios, selected_enfermidades, start_date, end_date):
        filtered_data = data_pieplot_1(data_inicio=start_date, data_fim=end_date,cidade=selected_municipios, enfermidade=selected_enfermidades)
        fig = pieplot_1(filtered_data)
        return fig



    ### --------------------------
    # Layout
    app.layout =  MantineProvider([
        html.Div([
            dmc.Grid([
                dmc.GridCol(col0, span=2.8),
                dmc.GridCol([ 
                    html.Div([
                        dmc.LoadingOverlay(
                            visible=False,
                            id="loading-overlay",
                            overlayProps={"radius": "sm", "blur": 1, "backgroundOpacity": 0.1},
                            loaderProps={"color": "#1b263b", "type": "oval"},
                        ),
                        col1
                    ], style={'position': 'relative'}),
                ], span=9),
            ], gutter="xs",align="stretch", justify='center')
        ])
    ])
    

    #-----------------------------------------
    ### Loading
    clientside_callback(
        """
        function(children) {
            return false;
        }
        """,
        Output("loading-overlay", "visible"),
        Input("grafico1", "figure"),
    )
    @app.callback(
        Output("loading-overlay", "visible"),
        Input('municipios-select', 'value'),
        Input('enfermidades-select', 'value'),
        Input('start-date', 'value'),
        Input('end-date', 'value'),
        prevent_initial_call=True
    )
    def show_loading_spinner(*_):
        # Aqui você pode fazer checagens extras se quiser
        # Mas como os callbacks principais já estão processando, você ativa loading
        return True  # Ativa o overlay enquanto os callbacks estão atualizando




    #-----------------------------------------
    @app.callback(
        Output('grafico1', 'figure'),
        Output('grafico_bar_3', 'figure'),
        Output('grafico_bar_4', 'figure'),
        Input('municipios-select', 'value'),
        Input('enfermidades-select', 'value'),
        Input('start-date', 'value'),
        Input('end-date', 'value'),
    )
    def update_graph(selected_municipios, selected_enfermidades, start_date, end_date):
        filtered_data = data_barplot_1(data_inicio=start_date, data_fim=end_date, cidade=selected_municipios, enfermidade=selected_enfermidades)
        fig = barplot_1(filtered_data)

        filtered_data = data_barplot_3(data_inicio=start_date, data_fim=end_date, cidade=selected_municipios, enfermidade=selected_enfermidades)
        fig_bar_3 = barplot_3(filtered_data)

        filtered_data = data_barplot_4(data_inicio=start_date, data_fim=end_date, cidade=selected_municipios, enfermidade=selected_enfermidades)
        fig_bar_4 = barplot_4(filtered_data)
        return fig, fig_bar_3, fig_bar_4
    

    return app.server