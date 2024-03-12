import pandas as pd
import plotly.express as px
from dash import Dash, html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc

# Load Data
data = pd.read_csv("team_project/data_cleaned.csv")
predict_data = pd.read_csv("team_project/data_cleaned.csv")

# Data Preprocessing
data["DATETIMEDATA"] = pd.to_datetime(data["DATETIMEDATA"], format="%Y-%m-%d %H:%M:%S")
data.sort_values("DATETIMEDATA", inplace=True)

# External CSS
external_stylesheets = [
    {
        "href": "https://fonts.googleapis.com/css2?family=Lato:wght@400;700&display=swap",
        "rel": "stylesheet",
    },
    "assets/style.css"  # Link to your CSS file
]

# Initialize the Dash app
app = Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title = "Air Quality Analytics"

# App layout
app.layout = html.Div(
    children=[
        html.Div(
            children=[
                html.P(children="☁️ Air Quality Analytics ☁️", className="header-emoji"),
                html.H1(children="Air Quality Analytics", className="header-title"),
            ],
            className="header",
        ),
        html.Div(
            children=[
                html.Div(
                    children=[
                        html.Div(children="Parameter", className="menu-title"),
                        dcc.Dropdown(
                            id="parameter-filter",
                            options=[
                                {"label": param, "value": param}
                                for param in data.columns[1:]
                            ],
                            value="PM25",
                            clearable=False,
                            className="dropdown",
                        ),
                    ]
                ),
                html.Div(
                    children=[
                        html.Div(
                            children="Date Range",
                            className="menu-title"
                        ),
                        dcc.DatePickerRange(
                            id="date-range",
                            min_date_allowed=data["DATETIMEDATA"].min().date(),
                            max_date_allowed=data["DATETIMEDATA"].max().date(),
                            start_date=data["DATETIMEDATA"].min().date(),
                            end_date=data["DATETIMEDATA"].max().date(),
                        ),
                    ]
                ),
            ],
            className="menu",
        ),
        html.Div(
            children=[
                html.Div(
                    children=dcc.Graph(
                        id="line-chart", config={"displayModeBar": False},
                    ),
                    className="card",
                ),
            ],
            className="wrapper",
        ),
        html.Div(
            children=[
                html.Div(
                    children=[
                        html.Div(
                            className="menu-title"
                        ),
                        html.Div(
                            id="stats-table",
                            className="stats-table",
                        ),
                    ],
                    className="card",
                    style={"width": "48%", "float": "right"},  # Add this line
                ),
                html.Div(
                    html.Div(
                        children=dcc.Graph(id="stats-chart"),
                    ),
                    className="card",
                    style={"width": "50%", "float": "left"},  # Add this line
                ),
            ],
            className="wrapper",
        ),
        html.Div(
                children=[
                    html.Div(
                        children=[
                            html.Div(children="Parameter", className="menu-title"),
                            dcc.Dropdown(
                                id="parameter-predict",
                                options=[
                                    {"label": param, "value": param}
                                    for param in predict_data.columns[1:]
                                ],
                                value="PM25",
                                clearable=False,
                                className="dropdown",
                            ),
                        ]
                    ),
                ],
                className= "menu"
        ),
        html.Div(
            children=[
                html.Div(
                    children=dcc.Graph(
                        id="predict-chart", config={"displayModeBar": False},
                    ),
                    className="card",
                ),
            ],
            className="wrapper",
        ),
    ]
)

# Callbacks
@app.callback(
    Output("line-chart", "figure"),
    [
        Input("parameter-filter", "value"),
        Input("date-range", "start_date"),
        Input("date-range", "end_date"),
    ],
)
def update_chart(selected_parameter, start_date, end_date):
    mask = (
        (data["DATETIMEDATA"] >= start_date)
        & (data["DATETIMEDATA"] <= end_date)
    )
    filtered_data = data.loc[mask]
    trace = {
        "x": filtered_data["DATETIMEDATA"],
        "y": filtered_data[selected_parameter],
        "type": "lines",
        "name": selected_parameter,
    }
    layout = {
        "title": f"{selected_parameter} over Time",
        "xaxis": {"title": "Datetime"},
        "yaxis": {"title": selected_parameter},
        "colorway": ["#29b6f6"],  # or any other color
    }
    return {"data": [trace], "layout": layout}

@app.callback(
    Output("stats-chart", "figure"),
    [
        Input("parameter-filter", "value"),
        Input("date-range", "start_date"),
        Input("date-range", "end_date"),
    ],
)
def update_stats_chart(selected_parameter, start_date, end_date):
    mask = (
        (data["DATETIMEDATA"] >= start_date)
        & (data["DATETIMEDATA"] <= end_date)
    )
    filtered_data = data.loc[mask]
    stats = filtered_data[selected_parameter].describe().reset_index().round(2)
    stats.columns = ["Statistic", "Value"]
    fig = px.bar(
        stats,
        x="Statistic",
        y="Value",
        title=f"Statistics - {selected_parameter} ({start_date}-{end_date})",
        color="Statistic",
    ).update_layout(plot_bgcolor="#F5F5F5")
    return fig

@app.callback(
    Output("stats-table", "children"),
    [
        Input("parameter-filter", "value"),
        Input("date-range", "start_date"),
        Input("date-range", "end_date"),
    ],
)
def update_stats_table(selected_parameter, start_date, end_date):
    mask = (
        (data["DATETIMEDATA"] >= start_date)
        & (data["DATETIMEDATA"] <= end_date)
    )
    filtered_data = data.loc[mask]
    stats = filtered_data[selected_parameter].describe().reset_index().round(2)
    stats.columns = ["Statistic", "Value"]
    stats_table = dbc.Table.from_dataframe(stats, striped=True, bordered=True, hover=True, className="custom-table")
    title = html.Div(children=f"Statistics - {selected_parameter} ({start_date}-{end_date})", className="menu-title")
    return [title, stats_table]

@app.callback(
    Output("predict-chart", "figure"),
    [
        Input("parameter-predict", "value"),
        Input("date-range", "start_date"),
        Input("date-range", "end_date"),
    ],
)
def update_predict_chart(selected_parameter, start_date, end_date):
    mask = (
        (data["DATETIMEDATA"] >= start_date)
        & (data["DATETIMEDATA"] <= end_date)
    )
    filtered_data = predict_data.loc[mask]
    trace = {
        "x": filtered_data["DATETIMEDATA"],
        "y": filtered_data[selected_parameter],
        "type": "lines",
        "name": selected_parameter,
    }
    layout = {
        "title": f"{selected_parameter} Prediction for the next week",
        "xaxis": {"title": "Datetime"},
        "yaxis": {"title": selected_parameter},
        "colorway": ["#ec407a"]
    }
    return {"data": [trace], "layout": layout}

if __name__ == "__main__":
    app.run_server(debug=True)
