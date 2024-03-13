import pandas as pd
import plotly.express as px
from dash import Dash, html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc

# Load Data
data = pd.read_csv("team_project/air4thai_44t_2024-02-01_2024-02-29.csv")

#data ส่วน Predict
predict_simulate = pd.read_csv("team_project/modelpm25_regression_simulate.csv")
predict_real = pd.read_csv("team_project/modelpm25_regression_real.csv")

#data ส่วน quality
quality_simulate = pd.read_csv("team_project/quality_of_modelpm25_regression_simulate.csv")
quality_real = pd.read_csv("team_project/quality_of_modelpm25_regression_real.csv")

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
        html.Div(style={'height': '30px'}),
        html.Div(
            children=[
                html.P(children="☁️ Air Quality Analytics ☁️", className="header-emoji"),
            ],
            className="header",
        ),
        # Add an empty div with height to create space
        html.Div(style={'height': '45px'}),  # Adjust height as needed
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
                html.Div(
                    children=[
                        html.Div(
                            children="Chart Type",
                            className="menu-title"
                        ),
                        dcc.Dropdown(
                            id="charttype",
                            options=[
                                {"label": "Line Chart", "value": "line"},
                                {"label": "Bar Chart", "value": "bar"},
                                {"label": "Scatter Plot", "value": "scatter"},
                            ],
                            value="line",
                            clearable=False,
                            className="dropdown",
                        ),
                    ]
                )
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
                                    for param in predict_simulate.columns[1:]
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
                            children="Chart Type",
                            className="menu-title"
                        ),
                        dcc.Dropdown(
                            id="chart-type1",
                            options=[
                                {"label": "Line Chart", "value": "line"},
                                {"label": "Bar Chart", "value": "bar"},
                                {"label": "Scatter Plot", "value": "scatter"},
                            ],
                            value="line",
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
                        id="predict-simulate", config={"displayModeBar": False},
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
                            html.Div(children="Parameter", className="menu-title"),
                            dcc.Dropdown(
                                id="parameter-predict",
                                options=[
                                    {"label": param, "value": param}
                                    for param in predict_simulate.columns[1:]
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
                            children="Chart Type",
                            className="menu-title"
                        ),
                        dcc.Dropdown(
                            id="chart-type2",
                            options=[
                                {"label": "Line Chart", "value": "line"},
                                {"label": "Bar Chart", "value": "bar"},
                                {"label": "Scatter Plot", "value": "scatter"},
                            ],
                            value="line",
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
                        id="quality-simulate", config={"displayModeBar": False},
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
                            html.Div(children="Parameter", className="menu-title"),
                            dcc.Dropdown(
                                id="parameter-predict",
                                options=[
                                    {"label": param, "value": param}
                                    for param in predict_simulate.columns[1:]
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
                            children="Chart Type",
                            className="menu-title"
                        ),
                        dcc.Dropdown(
                            id="chart-type3",
                            options=[
                                {"label": "Line Chart", "value": "line"},
                                {"label": "Bar Chart", "value": "bar"},
                                {"label": "Scatter Plot", "value": "scatter"},
                            ],
                            value="line",
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
                        id="predict-real", config={"displayModeBar": False},
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
                            html.Div(children="Parameter", className="menu-title"),
                            dcc.Dropdown(
                                id="parameter-predict",
                                options=[
                                    {"label": param, "value": param}
                                    for param in predict_simulate.columns[1:]
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
                            children="Chart Type",
                            className="menu-title"
                        ),
                        dcc.Dropdown(
                            id="chart-type4",
                            options=[
                                {"label": "Line Chart", "value": "line"},
                                {"label": "Bar Chart", "value": "bar"},
                                {"label": "Scatter Plot", "value": "scatter"},
                            ],
                            value="line",
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
                        id="quality-real", config={"displayModeBar": False},
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
        Input("charttype", "value"),
    ],
)
def update_chart(selected_parameter, start_date, end_date, chart_type):
    mask = (
        (data["DATETIMEDATA"] >= start_date)
        & (data["DATETIMEDATA"] <= end_date)
    )
    filtered_data = data.loc[mask]
    if chart_type == "line":
        trace = {
            "x": filtered_data["DATETIMEDATA"],
            "y": filtered_data[selected_parameter],
            "type": "line",
        }
    elif chart_type == "scatter":
        trace = {
            "x": filtered_data["DATETIMEDATA"],
            "y": filtered_data[selected_parameter],
            "mode": "markers",  # Scatter plot with markers
            "type": "scatter",
        }
    elif chart_type == "bar":
        trace = {
            "x": filtered_data["DATETIMEDATA"],
            "y": filtered_data[selected_parameter],
            "type": "bar",
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


#predict_simulate
@app.callback(
    Output("predict-simulate", "figure"),
    [
        Input("parameter-predict", "value"),
        Input("date-range", "start_date"),
        Input("date-range", "end_date"),
        Input("chart-type1", "value"),
    ],
)
def update_predict_chart(selected_parameter, start_date, end_date, chart_type):
    mask = (
        (data["DATETIMEDATA"] >= start_date)
        & (data["DATETIMEDATA"] <= end_date)
    )
    filtered_data = predict_simulate.loc[mask]
    if chart_type == "line":
        trace = {
            "x": filtered_data["DATETIMEDATA"],
            "y": filtered_data[selected_parameter],
            "type": "line",
        }
    elif chart_type == "scatter":
        trace = {
            "x": filtered_data["DATETIMEDATA"],
            "y": filtered_data[selected_parameter],
            "mode": "markers",  # Scatter plot with markers
            "type": "scatter",
        }
    elif chart_type == "bar":
        trace = {
            "x": filtered_data["DATETIMEDATA"],
            "y": filtered_data[selected_parameter],
            "type": "bar",
        }

    layout = {
        "title": f"{selected_parameter} Prediction Simulate",
        "xaxis": {"title": "Datetime"},
        "yaxis": {"title": selected_parameter},
        "colorway": ["#ec407a"]
    }
    return {"data": [trace], "layout": layout}


#quality_simulate
@app.callback(
    Output("quality-simulate", "figure"),
    [
        Input("parameter-predict", "value"),
        Input("date-range", "start_date"),
        Input("date-range", "end_date"),
        Input("chart-type2", "value"),
    ],
)
def quality_simulate_chart(selected_parameter, start_date, end_date, chart_type):
    mask = (
        (data["DATETIMEDATA"] >= start_date)
        & (data["DATETIMEDATA"] <= end_date)
    )
    filtered_data = quality_simulate.loc[mask]
    if chart_type == "line":
        trace = {
            "x": filtered_data["DATETIMEDATA"],
            "y": filtered_data[selected_parameter],
            "type": "line",
        }
    elif chart_type == "scatter":
        trace = {
            "x": filtered_data["DATETIMEDATA"],
            "y": filtered_data[selected_parameter],
            "mode": "markers",  
            "type": "scatter",
        }
    elif chart_type == "bar":
        trace = {
            "x": filtered_data["DATETIMEDATA"],
            "y": filtered_data[selected_parameter],
            "type": "bar",
        }

    layout = {
        "title": f"Quality of model {selected_parameter} simulate",
        "xaxis": {"title": "Datetime"},
        "yaxis": {"title": selected_parameter},
        "colorway": ["#ec407a"]
    }
    return {"data": [trace], "layout": layout}


#predict_real
@app.callback(
    Output("predict-real", "figure"),
    [
        Input("parameter-predict", "value"),
        Input("date-range", "start_date"),
        Input("date-range", "end_date"),
        Input("chart-type3", "value"),
    ],
)
def predict_real_chart(selected_parameter, start_date, end_date, chart_type):
    mask = (
        (data["DATETIMEDATA"] >= start_date)
        & (data["DATETIMEDATA"] <= end_date)
    )
    filtered_data = predict_real.loc[mask]
    if chart_type == "line":
        trace = {
            "x": filtered_data["DATETIMEDATA"],
            "y": filtered_data[selected_parameter],
            "type": "line",
        }
    elif chart_type == "scatter":
        trace = {
            "x": filtered_data["DATETIMEDATA"],
            "y": filtered_data[selected_parameter],
            "mode": "markers",  
            "type": "scatter",
        }
    elif chart_type == "bar":
        trace = {
            "x": filtered_data["DATETIMEDATA"],
            "y": filtered_data[selected_parameter],
            "type": "bar",
        }

    layout = {
        "title": f"{selected_parameter} Prediction Real",
        "xaxis": {"title": "Datetime"},
        "yaxis": {"title": selected_parameter},
        "colorway": ["#a3e9a4"]
    }
    return {"data": [trace], "layout": layout}


#quality_real
@app.callback(
    Output("quality-real", "figure"),
    [
        Input("parameter-predict", "value"),
        Input("date-range", "start_date"),
        Input("date-range", "end_date"),
        Input("chart-type4", "value"),
    ],
)
def quality_real_chart(selected_parameter, start_date, end_date, chart_type):
    mask = (
        (data["DATETIMEDATA"] >= start_date)
        & (data["DATETIMEDATA"] <= end_date)
    )
    filtered_data = quality_real.loc[mask]
    if chart_type == "line":
        trace = {
            "x": filtered_data["DATETIMEDATA"],
            "y": filtered_data[selected_parameter],
            "type": "line",
        }
    elif chart_type == "scatter":
        trace = {
            "x": filtered_data["DATETIMEDATA"],
            "y": filtered_data[selected_parameter],
            "mode": "markers",  
            "type": "scatter",
        }
    elif chart_type == "bar":
        trace = {
            "x": filtered_data["DATETIMEDATA"],
            "y": filtered_data[selected_parameter],
            "type": "bar",
        }

    layout = {
        "title": f"Quality of model {selected_parameter} real",
        "xaxis": {"title": "Datetime"},
        "yaxis": {"title": selected_parameter},
        "colorway": ["#a3e9a4"]
    }
    return {"data": [trace], "layout": layout}

if __name__ == "__main__":
    app.run_server(debug=True)
