import requests
import pandas as pd
from dash import dash, html, dash_table, dcc, callback, Output, Input
import plotly.express as px
import dash_mantine_components as dmc
import dash_bootstrap_components as dbc

# ฟังก์ชันดึงข้อมูลสถานี
def get_station_data(station_id, start_date="2023-12-29", end_date="2024-03-05"):
    datas = []
    param = "PM25,PM10,O3,CO,NO2,SO2,WS,TEMP,RH,WD"
    data_type = "hr"
    start_time = "00"
    end_time = "23"
    url = f"http://air4thai.com/forweb/getHistoryData.php?stationID={station_id}&param={param}&type={data_type}&sdate={start_date}&edate={end_date}&stime={start_time}&etime={end_time}"
    response = requests.get(url)
    response_json = response.json()
    for data in response_json["stations"][0]["data"]:
        data["stationID"] = response_json["stations"][0]["stationID"]
        datas.append(data)
    return datas

# ฟังก์ชันหลัก
def main(selected_stations=None):
    all_data = []
    if selected_stations:
        for station_id in selected_stations:
            station_data = get_station_data(station_id)
            all_data.extend(station_data)
            print(f"Retrieved data from station: {station_id}")
    else:
        print("No stations specified.")
    
    if all_data:
        pd_from_dict = pd.DataFrame.from_dict(all_data)
        pd_from_dict.to_csv("air4thai_44t_stations_data.csv", index=False)
        print("Data saved to air4thai_selected_stations_data.csv")
    else:
        print("No data retrieved.")

# ตัวแปรเก็บข้อมูล
data = []

# App Dash
app = dash.Dash(external_stylesheets=[dbc.themes.YETI, 'static/styles.css'])

# ดึงข้อมูลครั้งแรก
main(selected_stations=['44t'])

# อ่านข้อมูล CSV
df = pd.read_csv('air4thai_44t_stations_data.csv')

# ฟังก์ชันอัปเดตกราฟ
@app.callback(
    Output(component_id='graph-placeholder', component_property='figure'),
    Input(component_id='my-dmc-radio-item', component_property='value')
)

def update_graph():
    fig = px.line(df, x='DATETIMEDATA', y=['PM25'])
    fig.update_layout(
    xaxis_title="Date and Time",  # X-axis label
    yaxis_title="PM2.5",  # Y-axis label
)
    return fig

# ตารางข้อมูล
table = dbc.Card(
    [
        dash_table.DataTable(data=df.to_dict('records'), page_size=5, style_table={'overflowX': 'auto'})
    ], color= 'light', outline= True
)

# กราฟ
line_graph = dbc.Card(
    [
        dbc.CardBody([
            html.H1('PM 2.5 Graph', className='bold-text', style={'text-align': 'center'}),
            dcc.Graph(figure=update_graph(), id='graph-placeholder')
        ]), dbc.CardFooter(table)
    ], color="light", outline= True, class_name= "board-curved"
)   

# Assume line_graph is defined elsewhere in your code

app = dash.Dash(__name__)

app.layout = html.Div(
    [
        html.Div(html.H1('SETBACK PM 2.5', className='bold-text', style={'text-align': 'center'}), className='header'),
        dbc.Row([
            dbc.Col(html.Div(line_graph, className='graph-container'), width=5)
        ], justify='around')
    ]
)

# External CSS stylesheets
app.css.append_css({
    'external_url': 'https://stackpath.bootstrapcdn.com/bootstrap/4.5.0/css/bootstrap.min.css'
})

# Custom CSS
app.css.append_css({
    'external_url': '''
        .header {
            text-align: center;
            padding: 20px;
            background-color: #f8f9fa;
            border-bottom: 1px solid #ccc;
        }
        
        .graph-container {
            margin: 20px;
            padding: 20px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            border-radius: 5px;
            background-color: #ffffff;
        }
    '''
})

if __name__ == '__main__':
    app.run_server(debug=True)