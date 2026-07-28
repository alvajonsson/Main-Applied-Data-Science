# Import required libraries
import pandas as pd
import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import plotly.express as px


# =====================================
# Read SpaceX launch data
# =====================================

spacex_df = pd.read_csv("spacex_launch_dash.csv")


# Payload limits
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()



# =====================================
# Create Dash application
# =====================================

app = dash.Dash(__name__)



# =====================================
# Dashboard Layout
# =====================================

app.layout = html.Div(children=[

    html.H1(
        'SpaceX Launch Records Dashboard',
        style={
            'textAlign': 'center',
            'color': '#503D36',
            'font-size': 40
        }
    ),


    # Launch Site dropdown
    dcc.Dropdown(

        id='site-dropdown',

        options=[

            {
                'label': 'All Sites',
                'value': 'ALL'
            },

            {
                'label': 'CCAFS LC-40',
                'value': 'CCAFS LC-40'
            },

            {
                'label': 'CCAFS SLC-40',
                'value': 'CCAFS SLC-40'
            },

            {
                'label': 'KSC LC-39A',
                'value': 'KSC LC-39A'
            },

            {
                'label': 'VAFB SLC-4E',
                'value': 'VAFB SLC-4E'
            }

        ],

        value='ALL',

        placeholder="Select a Launch Site",

        searchable=True

    ),


    html.Br(),


    # Pie chart
    dcc.Graph(
        id='success-pie-chart'
    ),


    html.Br(),


    html.P(
        "Payload range (Kg):"
    ),


    # Payload slider
    dcc.RangeSlider(

        id='payload-slider',

        min=0,

        max=10000,

        step=1000,

        marks={
            0: '0',
            2500: '2500',
            5000: '5000',
            7500: '7500',
            10000: '10000'
        },

        value=[
            min_payload,
            max_payload
        ]

    ),


    html.Br(),


    # Scatter plot
    dcc.Graph(
        id='success-payload-scatter-chart'
    )


])




# =====================================
# Pie Chart Callback
# =====================================

@app.callback(

    Output(
        'success-pie-chart',
        'figure'
    ),

    Input(
        'site-dropdown',
        'value'
    )

)


def get_pie_chart(entered_site):


    # All sites selected
    if entered_site == 'ALL':


        # Keep only successful launches
        success_df = spacex_df[
            spacex_df['class'] == 1
        ]


        # Count successful launches by site
        site_success = success_df.groupby(
            'Launch Site'
        ).size().reset_index(
            name='Success Count'
        )


        fig = px.pie(

            site_success,

            values='Success Count',

            names='Launch Site',

            title='Launch Site Success Count'

        )


    else:


        # Selected site
        filtered_df = spacex_df[

            (spacex_df['Launch Site'] == entered_site)

            &

            (spacex_df['class'] == 1)

        ]


        site_success = filtered_df.groupby(
            'Launch Site'
        ).size().reset_index(
            name='Success Count'
        )


        fig = px.pie(

            site_success,

            values='Success Count',

            names='Launch Site',

            title=f'Success Launches for {entered_site}'

        )


    return fig




# =====================================
# Scatter Plot Callback
# =====================================

@app.callback(

    Output(
        'success-payload-scatter-chart',
        'figure'
    ),

    [

        Input(
            'site-dropdown',
            'value'
        ),

        Input(
            'payload-slider',
            'value'
        )

    ]

)


def get_scatter_plot(entered_site, payload_range):


    filtered_df = spacex_df[

        (spacex_df['Payload Mass (kg)'] >= payload_range[0])

        &

        (spacex_df['Payload Mass (kg)'] <= payload_range[1])

    ]


    if entered_site != 'ALL':

        filtered_df = filtered_df[

            filtered_df['Launch Site'] == entered_site

        ]



    fig = px.scatter(

        filtered_df,

        x='Payload Mass (kg)',

        y='class',

        color='Booster Version Category',

        title='Correlation between Payload and Success'

    )


    return fig




# =====================================
# Run Application
# =====================================

if __name__ == '__main__':

    app.run(
        debug=True,
        port=8050
    )