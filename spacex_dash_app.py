# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

ls = spacex_df['Launch Site'].unique().tolist()
lst = []
for l in ls:
    a = {'label':l,'value':l}
    lst.append(a)



# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(
    children=[
        html.H1(
            'SpaceX Launch Records Dashboard',
            style={'textAlign': 'center', 'color': '#503D36','font-size': 40}
        ),
        # TASK 1: Add a dropdown list to enable Launch Site selection
        # The default select value is for ALL sites
        dcc.Dropdown(id='site-dropdown',options=lst, placeholder='Select a Launch Site here', searchable=True),
        html.Br(),

        # TASK 2: Add a pie chart to show the total successful launches count for all sites
        # If a specific launch site was selected, show the Success vs. Failed counts for the site
        html.Div(dcc.Graph(id='success-pie-chart')),
        html.Br(),

        html.P("Payload range (Kg):"),
        # TASK 3: Add a slider to select payload range
        dcc.RangeSlider(id='payload-slider',min=0,max=10000,step=1000,value=[min_payload,max_payload]),
        html.Div(id='output-container-range-slider'),


        # TASK 4: Add a scatter chart to show the correlation between payload and launch success
        html.Div(dcc.Graph(id='success-payload-scatter-chart')),

        html.P("Which site has the largest successful launches? \n -KSC LC-39A"),
        html.P("Which site has the highest launch success rate?  \n -KSC LC-39A"),
        html.P("Which payload range(s) has the highest launch success rate?"),
        html.P("Which payload range(s) has the lowest launch success rate?"),
        html.P("Which F9 Booster version (v1.0, v1.1, FT, B4, B5, etc.) has the highest launch success rate?"),
    ]
)

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value'),
)
def getpie(value):
    data = spacex_df[spacex_df["Launch Site"]==value]
    outcome = data.groupby('class',as_index=False).count()
    outcome = outcome.rename(columns=({'Unnamed: 0':'count'}))
    outcome['class'] = outcome['class'].replace([0,1],['Failure','Success'])

    print(type(outcome['class']))
    print(type(outcome['class'].values.tolist()[0]))
    print(outcome['class'].values)
    
    fig = px.pie(outcome,names = outcome['class'].values,values=outcome['count'])
    return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'), Input(component_id="payload-slider", component_property="value")]
)
def getscatter(site,range):
    data = spacex_df[spacex_df["Launch Site"]==site]
    fil_data = data[data["Payload Mass (kg)"].between(range[0],range[1])]
    fig = px.scatter(
        fil_data, x="Payload Mass (kg)", y="class", 
        color="Booster Version", size=fil_data.index, 
        hover_data=['Booster Version'])
    return fig


@app.callback(
    Output(component_id='output-container-range-slider',component_property='children'),
    Input('payload-slider', 'value')
)
def update_output(value):
    return 'You have selected "{}"'.format(value)



# Run the app
if __name__ == '__main__':
    app.run_server()
