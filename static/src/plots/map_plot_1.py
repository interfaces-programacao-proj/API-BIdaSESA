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
        bgcolor="#eae0d5",
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
            font = dict(
                weight = 'bold',

            )  
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
        width = 350,
        plot_bgcolor='#eae0d5',
        paper_bgcolor='#eae0d5',
        dragmode = False
    )

    return fig


def barplot_ce(data, cidade='fortaleza'):
    data = data.groupby('nome_enfermidade').sum().reset_index()
    data.sort_values('quantidade', inplace=True, ascending=True)
    fig = go.Figure([
        go.Bar(
            y=data['nome_enfermidade'],
            x=data['quantidade'],
            text=data['quantidade'],
            orientation='h',
        )
    ])
    fig.update_traces(
        marker = dict(
            color = ['#415a77']*11+['#1b263b'],
        )
    )
    fig.update_layout(
        template = "simple_white",
        title = dict(
            text = f'Distribuição de enfermidades no municipio {cidade}',
            font = dict(
                weight = 'bold',
                family = "'inter', sans-serif",
                color = '#1b263b'
            )
        ),
        font = dict(
            family = "'inter', sans-serif",
        ),
        margin = dict(
            t = 50,
            b = 10,
            l = 10,
            r = 10
        ),

        xaxis = dict(
            visible = False
        ),
        plot_bgcolor='#eae0d5',
        paper_bgcolor='#eae0d5',
        height=340
    )
    fig.update_xaxes(
        color = '#1b263b'
    )

    return fig


def barplot11_ce(data, cidade='fortaleza'):
    data = data[::-1]
    fig = go.Figure([
        go.Bar(
            y=data['nome_enfermidade'],
            x=data['custo_total'],
            text=data['sum_humanize'],
            orientation='h',
        )
    ])
    fig.update_traces(
        hoverinfo = 'none',
        marker = dict(
            color = ['#415a77']*11+['#1b263b'],
        )
    )

    fig.update_layout(
        template = "simple_white",
        title = dict(
            text = f'Curto total de tratamentos no municipio {cidade}',
            font = dict(
                weight = 'bold',
                family = "'inter', sans-serif",
                color = '#1b263b'
            )
        ),
        font = dict(
            family = "'inter', sans-serif",
            
        ),
        margin = dict(
            t = 50,
            b = 10,
            l = 10,
            r = 10
        ),
        xaxis = dict(
            visible = False
        ),
        plot_bgcolor='#eae0d5',
        paper_bgcolor='#eae0d5'
    )
    fig.update_xaxes(
        color = '#1b263b'
    )

    return fig

def pie_hoverlabel(data, enfermidade ,cidade='fortaleza'):

    data = data.loc[data['nome_enfermidade'] == enfermidade].groupby('gravidade').sum().reset_index()

    fig = go.Figure([
        go.Pie(
            labels = data['gravidade'],
            values = data['quantidade'],
            textinfo = 'label+percent',
        )
    ])

    fig.update_traces(
        hoverinfo = 'none',
        marker = dict(
            colors = ["#778da9", "#1b263b","#e9edc9"]
        )
    )

    fig.update_layout(
        template = "simple_white",
        title = dict(
            text = f'Proporção de gravidade no municipio {cidade}',
            font = dict(
                weight = 'bold',
                family = "'inter', sans-serif",
                color = '#1b263b'
            )
        ),
        font = dict(
            family = "'inter', sans-serif",
        ),
        margin = dict(
            t = 50,
            b = 10,
            l = 10,
            r = 10
        ),
        width = 500,
        height = 300,
        dragmode = False,
        plot_bgcolor='#eae0d5',
        paper_bgcolor='#eae0d5'
    )

    return fig