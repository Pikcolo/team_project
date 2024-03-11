from dash import dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px
import dash_mantine_components as dmc
import dash_bootstrap_components as dbc


external_stylesheets = [
    {
        "href": "https://fonts.googleapis.com/css2?"
        "family=Lato:wght@400;700&display=swap",
        "rel": "stylesheet",
    },
]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

df = pd.read_csv('air4thai_44t_stations_data.csv')

@app.callback(
    Output(component_id='graph-placeholder', component_property='figure'),
    [Input('dummy-input', 'value')]  # Adding a dummy input
)
def update_graph(dummy_value):
    axis_label = px.line(df, x='DATETIMEDATA', y=['PM25'])
    axis_label.update_layout(
        xaxis_title="Date and Time",  # X-axis label
        yaxis_title="PM 2.5",  # Y-axis label
    )
    return axis_label

table = dbc.Card(
    [
        dash_table.DataTable(data=df.to_dict('records'), page_size=5, style_table={'overflowX': 'auto'})
    ], color='light', outline=True
)

line_graph = dbc.Card(
    [
        dbc.CardBody([
            html.H1('Line Graph'),
            dcc.Graph(figure=update_graph(None), id='graph-placeholder')  # Initial call with None
        ]), dbc.CardFooter(table)
    ], color="light", outline=True, class_name="board-curved"
)

app.layout = html.Div(
    [
        html.Div(html.H1('Regression PM 2.5', className='bold-text'), className='dash'),
        dcc.Input(id='dummy-input', style={'display': 'none'}),  # Dummy input with hidden style
        dbc.Row([
            dbc.Col(html.Div(line_graph, className='space-top'), width=5)
        ], justify='around')
    ]
)


if __name__ == '__main__':
    app.run_server(debug=True)
