# Import required libraries
import pandas as pd
import plotly.graph_objects as go
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output

# Read the airline data into pandas dataframe
airline_data =  pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/airline_data.csv', 
                            encoding = "ISO-8859-1",
                            dtype={'Div1Airport': str, 'Div1TailNum': str, 
                                   'Div2Airport': str, 'Div2TailNum': str})

# Create a dash application
app = dash.Dash(__name__)
                               
# 布局部分
app.layout = html.Div(children=[ 
    html.H1('Airline Performance Dashboard', style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),
    
    html.Div(["Input Year: ", dcc.Input(id='input-year', value='2010', type='number', style={'height':'50px', 'font-size': 35}),], 
             style={'font-size': 40}),
    html.Br(),
    html.Br(),
    html.Div(dcc.Graph(id='line-plot')),
])

# 回调函数装饰器 (把输入和输出绑定)
@app.callback( Output(component_id='line-plot', component_property='figure'),
               Input(component_id='input-year', component_property='value'))

# 核心计算并返回图表的函数
def get_graph(entered_year):
    # 筛选出输入的年份的数据
    df =  airline_data[airline_data['Year'] == int(entered_year)]
    
    # 按月份分组，计算平均延误时间
    line_data = df.groupby('Month')['ArrDelay'].mean().reset_index()

    # 画折线图
    fig = go.Figure(data=go.Scatter(x=line_data['Month'], y=line_data['ArrDelay'], mode='lines', marker=dict(color='green')))
    fig.update_layout(title='Month vs Average Flight Delay Time', xaxis_title='Month', yaxis_title='ArrDelay')
    return fig

# Run the app
if __name__ == '__main__':
    app.run()