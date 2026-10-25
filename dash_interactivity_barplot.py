# 1/ Import all the required libraries and read the dataset
import pandas as pd
import plotly.express as px  
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output

airline_data =  pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/airline_data.csv', 
                            encoding = "ISO-8859-1",
                            dtype={'Div1Airport': str, 'Div1TailNum': str, 
                                   'Div2Airport': str, 'Div2TailNum': str})

app = dash.Dash(__name__)

# 2/ 设置网页布局 (标题、输入框、图表)
app.layout = html.Div(children=[
    # 标题: Total number of flights to the destination state split by reporting airline, 字号40
    html.H1('Total number of flights to the destination state split by reporting airline', style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),
    
    # 输入框：id为 input-year, 默认 2010, 数字类型
    html.Div(["Input Year: ", dcc.Input(id='input-year', value='2010', type='number', style={'height':'50px', 'font-size': 35}),], 
             style={'font-size': 40}),
    
    html.Br(),
    html.Br(),
    
    # 图表：id 为 bar-plot
    html.Div(dcc.Graph(id='bar-plot')),
])

# 3/ 添加 Callback 装饰器
@app.callback( Output(component_id='bar-plot', component_property='figure'),
               Input(component_id='input-year', component_property='value') )

# 4/ 定义 Callback 函数绘制柱状图
def get_graph(entered_year):
    # 根据年份筛选数据
    df = airline_data[airline_data['Year'] == int(entered_year)]
    
    # 按目的地州 (DestState) 和 航空公司 (Reporting_Airline) 分组，计算航班数量
    bar_data = df.groupby(['DestState', 'Reporting_Airline'])['Flights'].sum().reset_index()
    
    # 使用 px.bar 画柱状图
    fig = px.bar(bar_data, x='DestState', y='Flights', color='Reporting_Airline', 
                 title='Total number of flights to the destination state split by reporting airline')
    
    # 更新 x 轴和 y 轴的标题
    fig.update_layout(xaxis_title='Destination State', yaxis_title='Number of Flights')
    
    return fig

# 5/ 运行 app
if __name__ == '__main__':
    # 强制关闭重载器，指定端口，这能防止在 Theia 终端里瞬间闪退
    app.run(debug=False, use_reloader=False, port=8051)