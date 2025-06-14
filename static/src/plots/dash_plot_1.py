import plotly.express as px
import plotly.graph_objects as go

def barplot_1(data):
    fig = go.Figure([
        go.Bar(
            x=data['nome'],
            y=data['incidencias'],
            text=data['incidencias'],
            orientation='v',
        )
    ])
    fig.update_traces(
        marker_color = "#0796D4",
        hovertemplate = "Quantidade de tratamentos: %{y}<extra></extra>"
    )
    fig.update_layout(
        template = "simple_white",
        title = dict(
            text = "Quantidade de tratamentos por cidade",
            font = dict(
                family = "inter, sans-serif",
                size = 16,
                weight='bold'
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
        height = 300
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
            colors = ["#FF4989", "#00A2FF"]
        )
    )
    fig.update_layout(
        template = "simple_white",
        title = dict(
            text = "Proporção enfermidade por genero",
            font = dict(
                family = "inter, sans-serif",
                size = 16,
                weight='bold'
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
        height = 300
    )
    return fig