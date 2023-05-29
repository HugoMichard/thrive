import pandas as pd
from dash import Dash, dcc, html, Input, Output, ctx
import plotly.graph_objects as go

app = Dash(__name__)


class Data:
    def __init__(self) -> None:
        self.load_data()
        self.load_logs()
        self.frame = 0

    def load_data(self):
        self.df = pd.read_csv('/home/hugo/Projects/thrive/frames.csv')
    
    def load_logs(self):
        self.logs = pd.read_csv('/home/hugo/Projects/thrive/logs.csv')
    
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

        min_range = min((df['x'] - df['size']).min(), (df['y'] - df['size']).min())
        max_range = max((df['x'] + df['size']).max(), (df['y'] + df['size']).max())

        # Set axes properties
        fig.update_xaxes(range=[min_range, max_range], zeroline=False)
        fig.update_yaxes(range=[min_range, max_range])

        for index, row in df.iterrows():
            r = row['size']
            color = f"#{row['color']}"
            fig.add_shape(type="circle",
                xref="x", yref="y",
                x0=row['x']-r, y0=row['y']-r, x1=row['x']+r, y1=row['y']+r,
                line_color=color,
                fillcolor=color
            )
    
        # Set figure size
        fig.update_layout(width=800, height=800)
        return fig

    def get_logs(self):
        logs = self.logs.loc[self.logs['frame'] == self.frame]
        return [html.Li(i) for i in ['Frame ' + str(self.frame)] + list(logs['log'])]


data = Data()

app.layout = html.Div([
    dcc.Graph(id="graph"),
    html.Div(
        children=[
            html.Ul(id='log-output', children=[])
        ],
    ),
    html.Button('Play', id='play'),
    dcc.Slider(0, 1000, 1,
               value=0,
               id='frame-slider'
    ),
    html.Button('Refresh', id='refresh-df'),
    dcc.Interval(
        id="play-interval", interval=1 * 1000, n_intervals=0
    ),
])


@app.callback(
    Output("graph", "figure"),
    Output("log-output", "children"),
    Input('frame-slider', 'value'),
    Input('refresh-df', 'n_clicks'),
    Input("play", "n_clicks"),
    Input("play-interval", "n_intervals"),
    prevent_initial_call=True)
def update_graph(slider_value, refresh_value, play_clicks, interval):
    triggered_id = ctx.triggered_id

    if triggered_id == 'frame-slider':
        data.frame = slider_value
    elif triggered_id == 'refresh-df':
        data.load_data()
    elif triggered_id == 'play-interval' and play_clicks is not None and play_clicks % 2 == 1:
        data.frame += 1
    
    return data.plot(), data.get_logs()


app.run_server(debug=True, use_reloader=False)  # Turn off reloader if inside Jupyter