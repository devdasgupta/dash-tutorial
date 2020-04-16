import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html

from dash.dependencies import Input, Output
# from mariner_telemetry.app import app

DATASOURCE = 'datatarget2020'

body = dbc.Container(
    dbc.Alert("Hello Bootstrap!", color="success"), className="p-5",
)

navbar = dbc.Navbar([
    # html.A(
        dbc.Col(
            [
                html.A(dbc.Row([dbc.NavbarBrand("Data Depth", className="col-md-2 bg-light")], no_gutters=True,)), href="https://plot.ly",
                dbc.Row([dbc.NavbarBrand("Data Breadth", className="col-md-2 bg-light")], no_gutters=True,),
            ],
            align="left",
        )
    # ),
    # href="https://google.com",
])

layout = html.Div(children=[
    html.Div(id=DATASOURCE + '_' + 'other graphs', children=navbar)
])
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = layout

if __name__ == "__main__":
    app.run_server()
