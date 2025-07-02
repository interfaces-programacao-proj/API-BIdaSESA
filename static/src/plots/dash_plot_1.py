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
        hovertemplate = "Quantidade de tratamentos: %{y}<extra></extra>",
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
        hovertemplate = "Custo total: %{x}<extra></extra>",
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
        marker = dict(
            color = ['#415a77']*6+['#1b263b'],
        ),
        hovertemplate = "Custo total: %{x}<extra></extra>",
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
