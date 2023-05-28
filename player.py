import pandas as pd
from dash import Dash, dcc, html, Input, Output, ctx
import plotly.graph_objects as go

app = Dash(__name__)


class Data:
    def __init__(self) -> None:
        self.load_data()        
        self.frame = 0

    def load_data(self):
        self.df = pd.read_csv('/home/hugo/Projects/thrive/frames.csv')
    
    def plot(self):
        df = self.df
        df = df.loc[df['frame'] == self.frame]

        fig = go.Figure()

        # Create scatter trace of text labels
        # fig.add_trace(go.Scatter(
        #     x=[1.5, 3.5],
        #     y=[0.75, 2.5],
        #     text=["Unfilled Circle",
        #           "Filled Circle"],
        #     mode="text",
        # ))

        # Set axes properties
        fig.update_xaxes(range=[(df['x'] - df['size']).min(), (df['x'] + df['size']).max()], zeroline=False)
        fig.update_yaxes(range=[(df['y'] - df['size']).min(), (df['y'] + df['size']).max()])

        for index, row in df.iterrows():
            r = row['size']
            fig.add_shape(type="circle",
                xref="x", yref="y",
                x0=row['x']-r, y0=row['y']-r, x1=row['x']+r, y1=row['y']+r,
                line_color="LightSeaGreen"
            )
    
        # Set figure size
        fig.update_layout(width=800, height=800)
        return fig


data = Data()


app.layout = html.Div([
    dcc.Graph(id="graph"),
    dcc.Slider(0, 1000, 1,
               value=0,
               id='frame-slider'
    ),
    html.Button('Refresh df', id='refresh-df')
])


@app.callback(
    Output("graph", "figure"), 
    Input('frame-slider', 'value'),
    Input('refresh-df', 'n_clicks'),
    prevent_initial_call=True)
def update_graph(slider_value, refresh_value):
    triggered_id = ctx.triggered_id
    print(triggered_id)

    if triggered_id == 'frame-slider':
        update_frame(slider_value)
    elif triggered_id == 'refresh-df':
        refresh_data()
    
    return data.plot()


def update_frame(frame):
    data.frame = frame


def refresh_data():
    data.load_data()


app.run_server(debug=True, use_reloader=False)  # Turn off reloader if inside Jupyter