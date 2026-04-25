import dash
from dash import dcc, html, Input, Output, State, callback_context
import plotly.graph_objects as go
import numpy as np

from simulation import check_win, add_computer_intelligently

app = dash.Dash(__name__)

# --- STYLING CONSTANTS ---
COLORS = {'X': 'red', 'O': 'blue', 'BG': '#1e1e1e'}
SCALE = {0: 0.4, 1: 0.25, 2: 0.12}
OPACITY = {0: 0.4, 1: 0.7, 2: 1.0}
OFFSET = {0: -0.05, 1: 0.0, 2: 0.05} # Tiny shift so points don't overlap perfectly

def create_figure(xs, os):
    fig = go.Figure()

    # 1. DRAW GHOST GRID (Clickable Targets)
    # We create a ghost grid for EACH W layer with a slight offset
    for w in [0, 1, 2]:
        ghost_x = []
        ghost_y = []
        ghost_z = []
        for z in range(3):
            for y in range(3):
                for x in range(3):
                    if [w, z, y, x] not in xs and [w, z, y, x] not in os:
                        ghost_x.append(x + OFFSET[w])
                        ghost_y.append(y + OFFSET[w])
                        ghost_z.append(z + OFFSET[w])

        fig.add_trace(go.Scatter3d(
            x=ghost_x, y=ghost_y, z=ghost_z,
            mode='markers',
            marker=dict(size=5, color='rgba(200,200,200,0.15)'),
            name=f"Available W={w}",
            hoverinfo='text',
            text=[f"W={w}, Z={int(z)}, Y={int(y)}, X={int(x)}" for z,y,x in zip(ghost_z, ghost_y, ghost_x)],
            customdata=[w] * len(ghost_x), # Store the W value here
            showlegend=False
        ))

    # 2. DRAW PLAYER MOVES (3D Meshes)
    def add_mesh_move(coords, color, name_prefix):
        for move in coords:
            w, z, y, x = move
            d = SCALE[w]
            # Center the shape on the offset coordinate
            cx, cy, cz = x + OFFSET[w], y + OFFSET[w], z + OFFSET[w]

            fig.add_trace(go.Mesh3d(
                x=[cx-d, cx-d, cx+d, cx+d, cx-d, cx-d, cx+d, cx+d],
                y=[cy-d, cy+d, cy+d, cy-d, cy-d, cy+d, cy+d, cy-d],
                z=[cz-d, cz-d, cz-d, cz-d, cz+d, cz+d, cz+d, cz+d],
                i=[7, 0, 0, 0, 4, 4, 6, 6, 4, 0, 3, 2],
                j=[3, 4, 1, 2, 5, 6, 5, 2, 0, 1, 6, 3],
                k=[0, 7, 2, 3, 6, 7, 1, 1, 5, 5, 7, 6],
                color=color, opacity=OPACITY[w],
                flatshading=True, showlegend=False
            ))

    add_mesh_move(xs, COLORS['X'], "X")
    add_mesh_move(os, COLORS['O'], "O")

    fig.update_layout(
        template='plotly_dark',
        margin=dict(l=0, r=0, b=0, t=40),
        scene=dict(
            xaxis=dict(range=[-0.5, 2.5], nticks=3),
            yaxis=dict(range=[-0.5, 2.5], nticks=3),
            zaxis=dict(range=[-0.5, 2.5], nticks=3),
            aspectmode='cube'
        ),
        clickmode='event+select'
    )
    return fig

# --- APP LAYOUT ---
app.layout = html.Div(style={'backgroundColor': COLORS['BG'], 'color': 'white', 'fontFamily': 'sans-serif', 'height': '100vh', 'padding': '20px'}, children=[
    html.H2("4D TIC-TAC-TOE: INTERACTIVE EDITION", style={'textAlign': 'center'}),
    html.Div([
        html.Button("RESET GAME", id='reset-btn', style={'marginRight': '10px'}),
        html.Span(id='status-text', style={'fontSize': '20px', 'fontWeight': 'bold'})
    ], style={'textAlign': 'center', 'marginBottom': '10px'}),

    dcc.Graph(id='game-graph', figure=create_figure([], []), config={'displayModeBar': False}),
    dcc.Store(id='game-store', data={'xs': [], 'os': [], 'winner': None})
])

# --- CALLBACKS ---
@app.callback(
    [Output('game-store', 'data'), Output('status-text', 'children')],
    [Input('game-graph', 'clickData'), Input('reset-btn', 'n_clicks')],
    [State('game-store', 'data')]
)
def update_game(clickData, n_clicks, data):
    ctx = callback_context
    if not ctx.triggered:
        return data, "Your turn, Player X!"

    trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]

    # Reset Game
    if trigger_id == 'reset-btn':
        return {'xs': [], 'os': [], 'winner': None}, "Game Reset. Player X's turn!"

    # Process Move
    if clickData and not data['winner']:
        pt = clickData['points'][0]
        # Extract original integer coordinates by rounding the offset values
        w = pt.get('customdata', 1) # Get W from customdata we stored
        z, y, x = int(round(pt['z'] - OFFSET[w])), int(round(pt['y'] - OFFSET[w])), int(round(pt['x'] - OFFSET[w]))
        move = [w, z, y, x]

        if move not in data['xs'] and move not in data['os']:
            # Player X Moves
            data['xs'].append(move)
            if check_win(data['xs']):
                data['winner'] = 'X'
                return data, "🏆 PLAYER X WINS!"

            # Computer Moves
            add_computer_intelligently(data['xs'], data['os'])
            if check_win(data['os']):
                data['winner'] = 'O'
                return data, "🤖 COMPUTER WINS!"

            return data, "Player X's turn..."

    return data, dash.no_update

@app.callback(
    Output('game-graph', 'figure'),
    Input('game-store', 'data')
)
def redraw_board(data):
    return create_figure(data['xs'], data['os'])

if __name__ == '__main__':
    app.run(debug=True)
