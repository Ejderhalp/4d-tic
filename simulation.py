### WELCOME TO 4D TIC TAC TOE ###

import numpy as np
from itertools import combinations
import plotly.graph_objects as go
import math
from dash import Dash, dcc, html, Input, Output, State, callback_context
import json

# game state
xs = []           # player X moves
os = []           # player O / computer moves
past_choices = [] # all played moves (to prevent duplicates)

# core game logic

def check_win(player_coords):
    if len(player_coords) < 3:
        return False
    for combo in combinations(player_coords, 3):
        win = True
        for dim in range(4):
            coords_in_dim = [p[dim] for p in combo]
            if not (coords_in_dim[0] == coords_in_dim[1] == coords_in_dim[2]
                    or coords_in_dim == [0, 1, 2]
                    or coords_in_dim == [2, 1, 0]):
                win = False
                break
        if win:
            return True
    return False

def final_move(choice, os_list):
    os_list.append(choice)
    past_choices.append(choice)

def add_computer_intelligently(xs, os):
    available = []
    for w in range(3):
        for z in range(3):
            for y in range(3):
                for x in range(3):
                    if [w, z, y, x] not in xs and [w, z, y, x] not in os:
                        available.append([w, z, y, x])

    if not available:
        return

    # 1. take a winning move if available
    for spot in available:
        if check_win(os + [spot]):
            final_move(spot, os)
            return

    # 2. block the player from winning
    for spot in available:
        if check_win(xs + [spot]):
            final_move(spot, os)
            return

    # 3. pick closest move to player's cluster
    best_move = None
    min_total_distance = float('inf')
    for spot in available:
        current_total_dist = sum(
            math.sqrt(sum((spot[i] - pm[i])**2 for i in range(4)))
            for pm in xs
        )
        if current_total_dist < min_total_distance:
            min_total_distance = current_total_dist
            best_move = spot

    if best_move:
        final_move(best_move, os)

# board visualisation

def build_figure(xs, os):
    fig = go.Figure()

    SCALE   = {0: 0.4,  1: 0.25, 2: 0.12}
    OPACITY = {0: 0.4,  1: 0.7,  2: 1.0}

    def draw_cube(x, y, z, size, color, opacity, name):
        d = size
        fig.add_trace(go.Mesh3d(
            x=[x-d,x-d,x+d,x+d,x-d,x-d,x+d,x+d],
            y=[y-d,y+d,y+d,y-d,y-d,y+d,y+d,y-d],
            z=[z-d,z-d,z-d,z-d,z+d,z+d,z+d,z+d],
            i=[7,0,0,0,4,4,6,6,4,0,3,2],
            j=[3,4,1,2,5,6,5,2,0,1,6,3],
            k=[0,7,2,3,6,7,1,1,5,5,7,6],
            color=color, opacity=opacity, name=name,
            flatshading=True, showlegend=False
        ))

    def draw_sphere(x, y, z, size, color, opacity, name):
        nb = 20
        phi, theta = np.meshgrid(
            np.linspace(0, 2*np.pi, nb),
            np.linspace(0, np.pi,   nb)
        )
        fig.add_trace(go.Surface(
            x=x + size*np.sin(theta)*np.cos(phi),
            y=y + size*np.sin(theta)*np.sin(phi),
            z=z + size*np.cos(theta),
            colorscale=[[0,color],[1,color]],
            showscale=False, opacity=opacity,
            name=name, hoverinfo='name'
        ))

    for move in xs:
        w, z, y, xc = move
        draw_cube(xc, y, z, SCALE[w], 'red', OPACITY[w], f"X (W={w})")

    for move in os:
        w, z, y, xc = move
        draw_sphere(xc, y, z, SCALE[w], 'blue', OPACITY[w], f"O (W={w})")

    # ghost grid
    ghost = [[z,y,x] for z in range(3) for y in range(3) for x in range(3)]
    fig.add_trace(go.Scatter3d(
        x=[c[2] for c in ghost],
        y=[c[1] for c in ghost],
        z=[c[0] for c in ghost],
        mode='markers',
        marker=dict(size=2, color='rgba(150,150,150,0.2)'),
        showlegend=False, hoverinfo='none'
    ))

    fig.update_layout(
        paper_bgcolor='#0f0f1a',
        plot_bgcolor='#0f0f1a',
        title=dict(
            text="4D Tic-Tac-Toe — size = 4th dimension (W)",
            font=dict(color='white', size=16)
        ),
        scene=dict(
            bgcolor='#0f0f1a',
            xaxis=dict(title='X', range=[-0.5,2.5], color='white'),
            yaxis=dict(title='Y', range=[-0.5,2.5], color='white'),
            zaxis=dict(title='Z', range=[-0.5,2.5], color='white'),
            aspectmode='cube',
            camera=dict(eye=dict(x=1.5,y=1.5,z=1.5))
        ),
        margin=dict(l=0, r=0, t=40, b=0),
        height=550,
    )
    return fig

# Dash app

app = Dash(__name__)

app.layout = html.Div(style={
    'backgroundColor': '#0f0f1a',
    'minHeight': '100vh',
    'fontFamily': '"Courier New", monospace',
    'color': 'white',
    'padding': '20px',
}, children=[

    # title
    html.H1("4D TIC-TAC-TOE", style={
        'textAlign': 'center',
        'letterSpacing': '8px',
        'fontSize': '2rem',
        'color': '#e0e0ff',
        'marginBottom': '4px',
    }),
    html.P("size = W dimension · red cubes = X · blue spheres = O", style={
        'textAlign': 'center',
        'color': '#666',
        'fontSize': '0.8rem',
        'marginBottom': '20px',
    }),

    # mode selector
    html.Div(style={'textAlign':'center','marginBottom':'16px'}, children=[
        html.Label("Game mode:", style={'marginRight':'10px','color':'#aaa'}),
        dcc.RadioItems(
            id='mode-selector',
            options=[
                {'label': ' 1 Player (vs Computer)', 'value': '1'},
                {'label': ' 2 Players',              'value': '2'},
            ],
            value='1',
            inline=True,
            style={'color':'white'},
            labelStyle={'marginRight':'20px'},
        ),
    ]),

    # board
    dcc.Graph(id='board', figure=build_figure([], []),
              config={'displayModeBar': False}),

    # status message
    html.Div(id='status', style={
        'textAlign': 'center',
        'fontSize': '1.2rem',
        'fontWeight': 'bold',
        'color': '#ff6666',
        'margin': '12px 0',
        'minHeight': '30px',
    }),

    # input row
    html.Div(style={
        'display': 'flex',
        'justifyContent': 'center',
        'alignItems': 'center',
        'gap': '12px',
        'marginBottom': '16px',
    }, children=[
        html.Div(id='turn-label', style={
            'color': '#aaa', 'fontSize': '0.95rem', 'whiteSpace': 'nowrap'
        }),
        dcc.Input(
            id='coord-input',
            type='text',
            placeholder='w z y x  (e.g. 0 1 2 1)',
            debounce=False,
            style={
                'backgroundColor': '#1a1a2e',
                'border': '1px solid #444',
                'color': 'white',
                'padding': '10px 14px',
                'borderRadius': '6px',
                'fontSize': '1rem',
                'width': '220px',
                'outline': 'none',
            }
        ),
        html.Button('SUBMIT', id='submit-btn', n_clicks=0, style={
            'backgroundColor': '#3333aa',
            'color': 'white',
            'border': 'none',
            'padding': '10px 24px',
            'borderRadius': '6px',
            'fontSize': '1rem',
            'cursor': 'pointer',
            'letterSpacing': '2px',
        }),
        html.Button('NEW GAME', id='reset-btn', n_clicks=0, style={
            'backgroundColor': '#1a1a1a',
            'color': '#aaa',
            'border': '1px solid #444',
            'padding': '10px 20px',
            'borderRadius': '6px',
            'fontSize': '0.9rem',
            'cursor': 'pointer',
        }),
    ]),

    # hidden state stores
    dcc.Store(id='game-state', data={
        'xs': [], 'os': [], 'past': [],
        'turn': 'X',      # whose turn: 'X' or 'O'
        'over': False,
    }),
])

# callback 

@app.callback(
    Output('board',       'figure'),
    Output('status',      'children'),
    Output('turn-label',  'children'),
    Output('coord-input', 'value'),
    Output('game-state',  'data'),
    Input('submit-btn',   'n_clicks'),
    Input('reset-btn',    'n_clicks'),
    State('coord-input',  'value'),
    State('mode-selector','value'),
    State('game-state',   'data'),
    prevent_initial_call=True,
)
def handle_move(submit_clicks, reset_clicks, raw_input, mode, state):
    ctx = callback_context
    triggered = ctx.triggered[0]['prop_id']

    # ── RESET ────────────────────────────────────────────────────────────────
    if 'reset-btn' in triggered:
        empty_state = {'xs':[],'os':[],'past':[],'turn':'X','over':False}
        return build_figure([],[]), '', 'Player X — enter your move:', '', empty_state

    # ── SUBMIT ───────────────────────────────────────────────────────────────
    if state['over']:
        return build_figure(state['xs'], state['os']), \
               'Game over! Press NEW GAME to play again.', '', '', state

    # parse input
    if not raw_input or not raw_input.strip():
        return build_figure(state['xs'], state['os']), \
               '⚠ Please enter 4 numbers (e.g. 0 1 2 1)', \
               f"Player {state['turn']} — enter your move:", '', state

    try:
        parts = raw_input.strip().split()
        if len(parts) != 4:
            raise ValueError
        move = [int(p) for p in parts]
        if not all(0 <= v <= 2 for v in move):
            raise ValueError
    except ValueError:
        return build_figure(state['xs'], state['os']), \
               '⚠ Invalid input — enter 4 numbers between 0 and 2', \
               f"Player {state['turn']} — enter your move:", raw_input, state

    # duplicate check
    if move in state['past'] or move in state['xs'] or move in state['os']:
        return build_figure(state['xs'], state['os']), \
               '⚠ That square is already taken!', \
               f"Player {state['turn']} — enter your move:", '', state

    xs_s   = state['xs']
    os_s   = state['os']
    past_s = state['past']
    turn   = state['turn']

    # ── PLAYER X MOVE ────────────────────────────────────────────────────────
    if turn == 'X':
        xs_s = xs_s + [move]
        past_s = past_s + [move]

        if check_win(xs_s):
            new_state = {'xs':xs_s,'os':os_s,'past':past_s,'turn':'X','over':True}
            return build_figure(xs_s, os_s), '🎉 Player X WINS!', '', '', new_state

        # 1-player: computer goes immediately
        if mode == '1':
            # run AI on temporary globals
            temp_xs = list(xs_s)
            temp_os = list(os_s)
            temp_past = list(past_s)

            available = []
            for w in range(3):
                for z in range(3):
                    for y in range(3):
                        for x in range(3):
                            if [w,z,y,x] not in temp_xs and [w,z,y,x] not in temp_os:
                                available.append([w,z,y,x])

            ai_move = None

            for spot in available:
                if check_win(temp_os + [spot]):
                    ai_move = spot
                    break

            if not ai_move:
                for spot in available:
                    if check_win(temp_xs + [spot]):
                        ai_move = spot
                        break

            if not ai_move:
                best = None
                min_d = float('inf')
                for spot in available:
                    d = sum(math.sqrt(sum((spot[i]-pm[i])**2 for i in range(4))) for pm in temp_xs)
                    if d < min_d:
                        min_d = d
                        best = spot
                ai_move = best

            if ai_move:
                temp_os   = temp_os + [ai_move]
                temp_past = temp_past + [ai_move]

            if check_win(temp_os):
                new_state = {'xs':temp_xs,'os':temp_os,'past':temp_past,'turn':'X','over':True}
                return build_figure(temp_xs, temp_os), '🤖 Computer WINS!', '', '', new_state

            new_state = {'xs':temp_xs,'os':temp_os,'past':temp_past,'turn':'X','over':False}
            return build_figure(temp_xs, temp_os), '', 'Player X — enter your move:', '', new_state

        # 2-player: switch to O
        new_state = {'xs':xs_s,'os':os_s,'past':past_s,'turn':'O','over':False}
        return build_figure(xs_s, os_s), '', 'Player O — enter your move:', '', new_state

    # ── PLAYER O MOVE (2-player only) ────────────────────────────────────────
    else:
        os_s   = os_s + [move]
        past_s = past_s + [move]

        if check_win(os_s):
            new_state = {'xs':xs_s,'os':os_s,'past':past_s,'turn':'X','over':True}
            return build_figure(xs_s, os_s), '🎉 Player O WINS!', '', '', new_state

        new_state = {'xs':xs_s,'os':os_s,'past':past_s,'turn':'X','over':False}
        return build_figure(xs_s, os_s), '', 'Player X — enter your move:', '', new_state


@app.callback(
    Output('turn-label', 'children', allow_duplicate=True),
    Input('mode-selector', 'value'),
    prevent_initial_call=True,
)
def update_label_on_mode_change(mode):
    return 'Player X — enter your move:'


if __name__ == '__main__':
    app.run(debug=False)
