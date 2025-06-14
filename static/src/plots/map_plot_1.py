import geobr 
import numpy as np
import plotly.graph_objects as go
from plotly.colors import n_colors
colors = n_colors('rgb(255, 240, 200)', 'rgb(255, 210, 150)', 12, colortype='rgb')[::-1]

geo_ce = geobr.read_municipality(code_muni='CE', simplified=True)

def map_plot_ce(data, geo_ce=geo_ce):
    geo_ce = geo_ce.merge(data, how='left', left_on='name_muni', right_on='nome_cidade', copy=False).fillna(0)


    geo_ce['geometry'] = geo_ce['geometry'].to_crs(epsg=4326)
    fig = go.Figure([
        go.Choropleth(
            geojson  = geo_ce.__geo_interface__,
            locations= geo_ce.index,
            text = geo_ce['name_muni'],
            z    = geo_ce['count'],
            colorscale = 'Reds',
        )
    ])
    fig.update_geos(
        center={"lat": -14, "lon": -55},
        fitbounds="locations",
        coastlinecolor="black",
        showrivers=True,            # Exibe rios no mapa
        rivercolor="blue",
        visible=False,
    )
    fig.update_traces(
        hovertemplate = '<b>Municipio</b> : %{text}<extra></extra>',
        hoverlabel = dict(
            bgcolor = "white",
            font = dict(
                family = "'inter', sans-serif",
                size = 16
            )  
        ),
        showscale=False,
    )
    fig.update_layout(
        title = dict(
            text = "Quantidade de tratamentos por cidade",  
        ),
        font = dict(
            family = "'inter', sans-serif",
        ),
        margin = dict(
            t = 30,
            b = 0,
            l = 0,
            r = 0
        ),
        width = 400,
        dragmode = False
    )

    return fig


def table_plot(data):
    data.rename(columns={'nome_enfermidade': 'Enfermidade', 'count': 'Quantidade de tratamentos', 'sum': 'Custo total'}, inplace=True)
    fig = go.Figure([
        go.Table(
            header=dict(
                values=data.columns.tolist()[:3],
                fill_color='deepskyblue',
                line_color='darkslategray',
                align='center',
                font=dict(
                    color='black', 
                    size =16,
                    family = "'inter', sans-serif",
                )
            ),
            cells=dict(
                values=[data[col] for col in data.columns[:3]],
                fill_color=[['white' for i in range(len(data))], 
                            np.array(colors)[data.rank_count-1],
                            np.array(colors)[data.rank_custo_total-1],
                            ],
                line_color='darkslategray',
                align='center',
                font=dict(
                    color='black', 
                    size =14,
                    family = "'inter', sans-serif",
                ),
                height=30
            )
        )
    ])
    fig.update_layout(
        font = dict(
            family = "'inter', sans-serif",
        ),
        margin = dict(
            t = 5,
            b = 5,
            l = 5,
            r = 5
        ),
    )
    return fig