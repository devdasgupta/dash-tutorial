"""
This app creates a simple sidebar layout using inline style arguments and the
dbc.Nav component.

dcc.Location is used to track the current location. There are two callbacks,
one uses the current location to render the appropriate page content, the other
uses the current location to toggle the "active" properties of the navigation
links.

For more details on building multi-page Dash applications, check out the Dash
documentation: https://dash.plot.ly/urls
"""
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

# link fontawesome to get the chevron icons
FA = "https://use.fontawesome.com/releases/v5.8.1/css/all.css"

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP, FA])

# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 12,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}


def create_progress_bar_layout(
    header=None,
    progress_label=None,
    progress_act_value=None,
    progress_perc_value=None,
    mode=None,
    x_axis_label=None
):
    """
    This function creates and return the label and progress bar for each element.
    This function can be called and based on the argument passed it would return the required dbc component
    :param x_axis_label: This is optional element which provides x axis label for progress bar
    :param progress_perc_value: progress percentage value
    :param progress_label: The name of the progress bar
    :param progress_act_value: The progress actual value
    :param header: The header section of progress bar
    :return: dbc component for building the webpage
    """
    if header is not None:
        return html.H5(children=header)
    elif all([progress_label, progress_act_value, progress_perc_value, mode]):
        progress_display = f'{progress_perc_value}%' if mode == 'percentage' else f'{progress_act_value}K'

        if x_axis_label is not None:
            return dbc.Row([
                dbc.Col([
                    html.P(children=progress_label)
                ], width='3'),
                dbc.Col([
                    dbc.Progress(f"{progress_display}", value=progress_perc_value, style={"height": "25px"}),
                    dbc.Row(x_axis_label)
                ], width='8')
            ])
        else:
            return dbc.Row([
                dbc.Col([
                    html.P(children=progress_label)
                ], width='3'),
                dbc.Col([
                    dbc.Progress(f"{progress_display}", value=progress_perc_value, style={"height": "25px"})
                ], width='8')
            ])
    else:
        return None

nav_item = dbc.NavItem(dbc.NavLink("Link", href="#"))
default = dbc.NavbarSimple(
    children=[nav_item],
    brand="Dashboard Title",
    brand_href="#",
    sticky="top",
    className="mb-5",
)

submenu_1 = [
    html.Li(
        # use Row and Col components to position the chevrons
        dbc.Row(
            [
                dbc.Col("Menu 1"),
                dbc.Col(
                    html.I(className="fas fa-chevron-right mr-3"), width="auto"
                ),
            ],
            className="my-1",
        ),
        id="submenu-1",
    ),
    # we use the Collapse component to hide and reveal the navigation links
    dbc.Collapse(
        [
            dbc.NavLink("Page 1.1", href="/page-1/1"),
            dbc.NavLink("Page 1.2", href="/page-1/2"),
        ],
        id="submenu-1-collapse",
    ),
]

submenu_2 = [
    html.Li(
        dbc.Row(
            [
                dbc.Col("Menu 2"),
                dbc.Col(
                    html.I(className="fas fa-chevron-right mr-3"), width="auto"
                ),
            ],
            className="my-1",
        ),
        id="submenu-2",
    ),
    dbc.Collapse(
        [
            dbc.NavLink("Page 2.1", href="/page-2/1"),
            dbc.NavLink("Page 2.2", href="/page-2/2"),
        ],
        id="submenu-2-collapse",
    ),
]


sidebar = html.Div(
    [
        html.H2("Sidebar", className="display-4"),
        html.Hr(),
        html.P(
            "A sidebar with collapsible navigation links", className="lead"
        ),
        dbc.Nav(submenu_1 + submenu_2, vertical=True),
    ],
    style=SIDEBAR_STYLE,
    id="sidebar",
)

content = html.Div(id="page-content", style=CONTENT_STYLE)

app.layout = html.Div([dcc.Location(id="url"), default, sidebar, content])


# this function is used to toggle the is_open property of each Collapse
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


# this function applies the "open" class to rotate the chevron
def set_navitem_class(is_open):
    if is_open:
        return "open"
    return ""


for i in [1, 2]:
    app.callback(
        Output(f"submenu-{i}-collapse", "is_open"),
        [Input(f"submenu-{i}", "n_clicks")],
        [State(f"submenu-{i}-collapse", "is_open")],
    )(toggle_collapse)

    app.callback(
        Output(f"submenu-{i}", "className"),
        [Input(f"submenu-{i}-collapse", "is_open")],
    )(set_navitem_class)

progress_label = 'Some Label'
progress_display = '10'
progress_perc_value = int(progress_display)
x_axis_label = [
    html.P(children=0, style={"float": "left", "width": "50%", "text-align": "left"}),
    html.P(children=20, style={"float": "left", "width": "50%", "text-align": "right"}),
]

@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):

    if pathname in ["/", "/page-1/1"]:
        return dbc.Row([
            dbc.Col([
                html.P(children=progress_label)
            ], width='3'),
            dbc.Col([
                # html.Div([Progress(id="progress", percent=progress_value, strokeWidth=20)])
                dbc.Progress(f"{progress_display}", value=progress_perc_value, style={"height": "25px"}),
                dbc.Row([
                    html.P(children=0, style={"float": "left", "width": "50%", "text-align": "left"}),
                    html.P(children=100, style={"float": "left", "width": "50%", "text-align": "right"})
                ])
            ], width='8')
        ])
    elif pathname == "/page-1/2":
        return create_progress_bar_layout(progress_label=progress_label, progress_act_value=progress_display, progress_perc_value=progress_perc_value, mode='percentage', x_axis_label=x_axis_label)
    elif pathname == "/page-2/1":
        return html.P("Oh cool, this is page 2.1!")
    elif pathname == "/page-2/2":
        return html.P("No way! This is page 2.2!")
    # If the user tries to reach a different page, return a 404 message
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    )


if __name__ == "__main__":
    app.run_server(port=8887, debug=True)
