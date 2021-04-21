import pandas as pd
import pathlib
from dash import Dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px

app = Dash(__name__)

# Importing Data
PATH = pathlib.Path(__file__).parent
PATH = PATH.joinpath('Dataset')
df = pd.read_excel(PATH.joinpath('ICC Test Bat 3001.xlsx'))

# Cleaning Data
for i in range(len(df['HS'])):
    if '*' in str(df['HS'][i]):
        df['HS'][i] = df['HS'][i].rstrip('*')

to_delete = df[df['Runs'] == '-'].index
df.drop(to_delete, inplace=True)
cleaned_data = df.drop(['Span', 'Player Profile'], axis=1)

# App Layout
app.layout = html.Div([

    html.H1('Cricket Dashboard', style={'text-align': 'center'}),

    dcc.Dropdown(id='player_list',
                 options=[{'label': i, 'value': i} for i in cleaned_data.columns.difference(['Player'])],
                 multi=False,
                 value='Select',
                 style={'width': '40%'}
                 ),

    html.Div(id='output_container', children=[]),
    html.Br(),

    dcc.Graph(id='cricket_chart', figure={})

])


# Connecting dcc components to the graph
@app.callback(
    [Output(component_id='output_container', component_property='children'),
     Output(component_id='cricket_chart', component_property='figure')],
    [Input(component_id='player_list', component_property='value')]
)
def update_graph(selected_player):
    container = f'The player selected is {selected_player}'

    df_copy = cleaned_data.copy()
    # df_copy.set_index('Player', inplace=True, drop=True)
    df_copy = df_copy[df_copy[selected_player]]

    fig = px.bar(data_frame=df_copy, x='Player', y='Runs', color='Player')

    return container, fig


if __name__ == '__main__':
    app.run_server(debug=True)
