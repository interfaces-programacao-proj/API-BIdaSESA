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
        plot_bgcolor='#eae0d5',
        paper_bgcolor='#eae0d5'
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
        plot_bgcolor='#eae0d5',
        paper_bgcolor='#eae0d5'
    )
    return fig