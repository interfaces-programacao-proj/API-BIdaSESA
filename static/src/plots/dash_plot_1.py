import plotly.express as px
import plotly.graph_objects as go

def barplot_1(data):
    fig = go.Figure([
        go.Bar(
            x=data['nome'],
            y=data['incidencias'],
            orientation='v',
        )
    ])
    fig.update_traces(
        marker = dict(
            color = ['#1b263b']+['#415a77']*12,
        ),
        hovertemplate = "<b>Quantidade de tratamentos :</b> %{y}<extra></extra>",
        hoverlabel = dict(
            bgcolor = "white",
            font = dict(
                family = "inter, sans-serif",
                size = 12
            )
        )
    )
    fig.update_layout(
        template = "simple_white",
        title = dict(
            text = "Quantidade de tratamentos por cidade",
            font = dict(
                family = "inter, sans-serif",
                size = 16,
                weight='bold',
                color = '#1b263b'
            )
        ),
        font = dict(
            family = "inter, sans-serif",
            size = 12
        ),
        margin = dict(
            l = 10,
            r = 10,
            t = 50,
            b = 0
        ),
        dragmode=False,
        height = 300,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
    )
    return fig



# ---------------------- PIZZA ----------------------
def pieplot_1(data):
    fig = go.Figure([
        go.Pie(
            labels = data['sexo'],
            values = data['count'],
            textinfo = 'label+percent',
        )
    ])
    fig.update_traces(
        marker = dict(
            colors = ["#bc4749", "#003049"]
        )
    )
    fig.update_layout(
        template = "simple_white",
        title = dict(
            text = "Proporção enfermidade por genero",
            font = dict(
                family = "'inter', sans-serif",
                size = 16,
                weight='bold',
                color = '#1b263b'
            )
        ),
        font = dict(
            family = "'inter', sans-serif",
            size = 12
        ),
        margin = dict(
            l = 10,
            r = 10,
            t = 50,
            b = 0
        ),
        dragmode=False,
        height = 300,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
    )
    return fig




#---------------------- BAR PLOT ----------------------
## Faixa etaria x custo
def barplot_3(data):
    data = data[::-1]
    fig = go.Figure([
        go.Bar(
            y=data['faixa'],
            x=data['custo_total'],
            text=data['custo_total_cat'],
            orientation='h',
        )
    ])
    fig.update_traces(
        marker = dict(
            color = ['#415a77']*6+['#1b263b'],
        ),
        hovertemplate = "Custo total: %{x}  <extra></extra>",
        hoverlabel = dict(
            bgcolor = "white",
            font = dict(
                family = "inter, sans-serif",
                size = 12
            )
        )
    )
    fig.update_layout(
        template = "simple_white",
        title = dict(
            text = "Custo total por faixa etaria",
            font = dict(
                family = "inter, sans-serif",
                size = 16,
                weight='bold',
                color = '#1b263b'
            )
        ),
        font = dict(
            family = "inter, sans-serif",
            size = 12
        ),
        margin = dict(
            l = 10,
            r = 10,
            t = 50,
            b = 0
        ), 
        dragmode=False,
        height = 300,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
    )
    fig.update_xaxes(
        visible=False
    )
    return fig



#---------------------- BAR PLOT ----------------------

def barplot_4(data):
    data = data[::-1]
    fig = go.Figure([
        go.Bar(
            y=data['faixa'],
            x=data['tempo_medio'],
            text=data['tempo_medio_cat'],
            orientation='h',
        )
    ])
    fig.update_traces(
        hoverinfo = 'none',
        marker = dict(
            color = ['#415a77']*6+['#1b263b'],
        ),
    )
    fig.update_layout(
        template = "simple_white",
        title = dict(
            text = "Tempo médio de tratamento por faixa etaria",
            font = dict(
                family = "inter, sans-serif",
                size = 16,
                weight='bold',
                color = '#1b263b'
            )
        ),
        font = dict(
            family = "inter, sans-serif",
            size = 12
        ),
        margin = dict(
            l = 10,
            r = 10,
            t = 50,
            b = 0
        ),
        
        dragmode=False,
        height = 300,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
    )
    fig.update_xaxes(
        visible=False
    )
    return fig



#---------------------- LINE PLOT ----------------------

def lineplot_1(data):
    data['count_suavizado'] = data['count'].ewm(span=3, adjust=False).mean()
    data['média_movel'    ] = data['count'].rolling(30).mean() 
    fig = go.Figure([
        go.Scatter(
            x=data['data_inicio'],
            y=data['count_suavizado'],
            customdata = round(data['count'], 2),
            mode='lines',
            line=dict(color='#1b263b'),
            name = 'Caso total suavizado',
            hovertemplate = '<b>Quantidade de casos : %{customdata}</b> <br>data : %{x}<extra></extra>'
        )
    ])

    fig.add_traces([
        go.Scatter(
            x=data['data_inicio'],
            y=data['média_movel'],
            customdata = round(data['média_movel'], 2),
            mode='lines',
            line=dict(
                color='#c1121f',
                width=2
            ),
            name = 'Média móvel de caso total',
            hovertemplate = '<b>Quantidade média de casos : %{customdata}</b> <br>data : %{x}<extra></extra>'
        )   
    ])

    fig.update_traces(
        hoverlabel = dict(
            bgcolor = 'white',
            font = dict(
                family = "inter, sans-serif",
                size = 14
            )
        ),
        hovertemplate = 'Quantidade de casos : %{customdata} <br>data : %{x}<extra></extra>'
    )
    fig.update_layout(
        template = "simple_white",
        title = dict(
            text = "Série histórica de casos",
            font = dict(
                family = "inter, sans-serif",
                size = 16,
                weight='bold',
                color = '#1b263b'
            )
        ),
        font = dict(
            family = "inter, sans-serif",
            size = 12
        ),
        margin = dict(
            l = 10,
            r = 10,
            t = 50,
            b = 0
        ),
        legend = dict(
            x = 0.5,
            y = 1.2
        ),
        dragmode=False,
        height = 300,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',

    )
    return fig


#---------------------- PIE PLOT ----------------------

def barplot_5(data):
    fig = go.Figure([])
    cores = {'Leve': '#778da9', 'Grave': '#606c38', 'Muito Grave': '#780000'}
    for gravidade, data in data.groupby('gravidade'):
        fig.add_trace(
            go.Bar(
                x = data['faixa'],
                y = data['casos_total'],
                name = gravidade,
                hovertemplate = '<b>Quantidade de casos : %{y}</b> <br>faixa : %{x} <br> Tipo:' + gravidade + '<extra></extra>',
                marker = dict(
                    color = cores.get(gravidade,'#1b263b')
                )
            )
        )
    
    fig.update_traces(
        hoverlabel = dict(
            bgcolor = 'white'
        )
    )

    fig.update_layout(
        template='simple_white',
        barmode='stack',
        hovermode='x unified',
        title = dict(
            text = "Tempo médio de tratamento por faixa etaria",
            font = dict(
                family = "inter, sans-serif",
                size = 16,
                weight='bold',
                color = '#1b263b'
            )
        ),
        font = dict(
            family = "inter, sans-serif",
            size = 12
        ),
        margin = dict(
            l = 10,
            r = 10,
            t = 50,
            b = 0
        ),
        dragmode=False,
        height = 300,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',

    )
    return fig


#---------------------- PIE PLOT ----------------------

def barplot_6(data):
    fig = go.Figure([])
    cores = {'Leve': '#778da9', 'Grave': '#606c38', 'Muito Grave': '#780000'}
    for gravidade, data in data.groupby('gravidade'):
        string_ = '<b>Quantidade de casos : %{y}</b> <br>faixa : %{x} <br> Tipo:' + gravidade + '<extra></extra>'
        fig.add_trace(
            go.Bar(
                x = data['faixa'],
                y = data['custo_médio'],
                name = gravidade,
                hovertemplate = string_,
                marker = dict(
                    color = cores.get(gravidade,'#1b263b')
                )
            )
        )
    
    fig.update_traces(
        hoverlabel = dict(
            bgcolor = 'white'
        )
    )

    fig.update_layout(
        template='simple_white',
        hovermode='x unified',
        title = dict(
            text = "Custo médio por faixa etária",
            font = dict(
                family = "inter, sans-serif",
                size = 16,
                weight='bold',
                color = '#1b263b'
            )
        ),
        font = dict(
            family = "inter, sans-serif",
            size = 12
        ),
        margin = dict(
            l = 10,
            r = 10,
            t = 50,
            b = 0
        ),
        dragmode=False,
        height = 300,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
    )
    return fig