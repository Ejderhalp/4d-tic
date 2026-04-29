### WELCOME TO 4D TIC TAC TOE ###

import numpy as np
from itertools import combinations
import plotly.graph_objects as go
import math
from dash import Dash, dcc, html, Input, Output, State, callback_context

app = Dash(__name__)

# ── game logic ────────────────────────────────────────────────────────────────

def check_win(player_coords):
    if len(player_coords) < 3:
        return False
    for combo in combinations(player_coords, 3):
        win = True
        for dim in range(4):
            c = [p[dim] for p in combo]
            if not (c[0]==c[1]==c[2] or c==[0,1,2] or c==[2,1,0]):
                win = False
                break
        if win:
            return True
    return False

def get_ai_move(xs, os):
    available = [[w,z,y,x] for w in range(3) for z in range(3)
                            for y in range(3) for x in range(3)
                            if [w,z,y,x] not in xs and [w,z,y,x] not in os]
    if not available:
        return None
    for spot in available:
        if check_win(os + [spot]):
            return spot
    for spot in available:
        if check_win(xs + [spot]):
            return spot
    return min(available, key=lambda s: sum(
        math.sqrt(sum((s[i]-p[i])**2 for i in range(4))) for p in xs
    ))

# ── board visualisation ───────────────────────────────────────────────────────

def build_figure(xs, os):
    fig = go.Figure()
    SCALE   = {0:0.4, 1:0.25, 2:0.12}
    OPACITY = {0:0.4, 1:0.7,  2:1.0}

    def draw_cube(x, y, z, s, col, op, name):
        d = s
        fig.add_trace(go.Mesh3d(
            x=[x-d,x-d,x+d,x+d,x-d,x-d,x+d,x+d],
            y=[y-d,y+d,y+d,y-d,y-d,y+d,y+d,y-d],
            z=[z-d,z-d,z-d,z-d,z+d,z+d,z+d,z+d],
            i=[7,0,0,0,4,4,6,6,4,0,3,2],
            j=[3,4,1,2,5,6,5,2,0,1,6,3],
            k=[0,7,2,3,6,7,1,1,5,5,7,6],
            color=col, opacity=op, name=name, flatshading=True, showlegend=False
        ))

    def draw_sphere(x, y, z, s, col, op, name):
        phi, theta = np.meshgrid(np.linspace(0,2*np.pi,20), np.linspace(0,np.pi,20))
        fig.add_trace(go.Surface(
            x=x+s*np.sin(theta)*np.cos(phi),
            y=y+s*np.sin(theta)*np.sin(phi),
            z=z+s*np.cos(theta),
            colorscale=[[0,col],[1,col]], showscale=False,
            opacity=op, name=name, hoverinfo='name'
        ))

    for w,z,y,x in xs:
        draw_cube(x, y, z, SCALE[w], 'red',  OPACITY[w], f"X (W={w})")
    for w,z,y,x in os:
        draw_sphere(x, y, z, SCALE[w], 'blue', OPACITY[w], f"O (W={w})")

    ghost = [[z,y,x] for z in range(3) for y in range(3) for x in range(3)]
    fig.add_trace(go.Scatter3d(
        x=[c[2] for c in ghost], y=[c[1] for c in ghost], z=[c[0] for c in ghost],
        mode='markers', marker=dict(size=2, color='rgba(150,150,150,0.2)'),
        showlegend=False, hoverinfo='none'
    ))

    fig.update_layout(
        paper_bgcolor='#0f0f1a', height=520,
        title=dict(text="4D Tic-Tac-Toe — size = W dimension", font=dict(color='white')),
        scene=dict(
            bgcolor='#0f0f1a',
            xaxis=dict(title='X', range=[-0.5,2.5], color='white'),
            yaxis=dict(title='Y', range=[-0.5,2.5], color='white'),
            zaxis=dict(title='Z', range=[-0.5,2.5], color='white'),
            aspectmode='cube', camera=dict(eye=dict(x=1.5,y=1.5,z=1.5))
        ),
        margin=dict(l=0,r=0,t=40,b=0),
    )
    return fig

def build_move_log(xs, os):
    # builds the move history panel content
    def move_rows(moves, color, label):
        if not moves:
            return [html.P('No moves yet', style={'color':'#555','fontSize':'0.8rem','margin':'4px 0'})]
        return [
            html.P(f"{i+1}. [{m[0]} {m[1]} {m[2]} {m[3]}]",
                   style={'color': color, 'margin':'3px 0', 'fontSize':'0.85rem'})
            for i, m in enumerate(moves)
        ]

    return html.Div(children=[
        # X moves
        html.P("PLAYER X", style={'color':'#ff6666','letterSpacing':'2px',
                                   'fontSize':'0.75rem','marginBottom':'6px','fontWeight':'bold'}),
        *move_rows(xs, '#ff9999', 'X'),
        html.Hr(style={'borderColor':'#333','margin':'10px 0'}),
        # O moves
        html.P("PLAYER O", style={'color':'#6699ff','letterSpacing':'2px',
                                   'fontSize':'0.75rem','marginBottom':'6px','fontWeight':'bold'}),
        *move_rows(os, '#99bbff', 'O'),
    ])

# ── layout ────────────────────────────────────────────────────────────────────

S = {'backgroundColor':'#0f0f1a','color':'white','fontFamily':'"Courier New",monospace'}

app.layout = html.Div(style={**S,'minHeight':'100vh','padding':'20px'}, children=[

    html.H1("4D TIC-TAC-TOE", style={'textAlign':'center','letterSpacing':'8px','color':'#e0e0ff'}),
    html.P("red cubes = X · blue spheres = O · size = W dimension",
           style={'textAlign':'center','color':'#666','fontSize':'0.8rem'}),

    # mode toggle
    html.Div(style={'textAlign':'center','marginBottom':'16px'}, children=[
        html.Label('GAME MODE', style={'color':'#aaa','letterSpacing':'3px','fontSize':'0.75rem','display':'block','marginBottom':'8px'}),
        dcc.RadioItems(id='mode', options=[
            {'label':' 1 Player (vs Computer)','value':'1'},
            {'label':' 2 Players','value':'2'},
        ], value='1', inline=True,
        labelStyle={'marginRight':'24px','fontSize':'1rem','color':'#e0e0ff','cursor':'pointer'},
        inputStyle={'marginRight':'6px'},
        style={'color':'#e0e0ff'}),
    ]),

    # main row: board + move log side by side
    html.Div(style={'display':'flex','alignItems':'flex-start','gap':'16px'}, children=[

        # board takes most of the space
        html.Div(style={'flex':'1'}, children=[
            dcc.Graph(id='board', figure=build_figure([],[]), config={'displayModeBar':False}),
        ]),

        # move log panel in the upper right
        html.Div(id='move-log', style={
            'width':'180px',
            'backgroundColor':'#12121f',
            'border':'1px solid #2a2a4a',
            'borderRadius':'8px',
            'padding':'14px',
            'marginTop':'40px',
            'minHeight':'200px',
            'flexShrink':'0',
        }, children=build_move_log([], [])),
    ]),

    html.Div(id='status', style={'textAlign':'center','fontSize':'1.2rem',
                                  'fontWeight':'bold','color':'#ff6666','margin':'12px 0'}),

    # input row
    html.Div(style={'display':'flex','justifyContent':'center','gap':'12px','alignItems':'center'}, children=[
        html.Div(id='turn-label', style={'color':'#aaa','whiteSpace':'nowrap'}),
        dcc.Input(id='coord-input', type='text', placeholder='w z y x  (e.g. 0 1 2 1)',
                  style={**S,'border':'1px solid #444','padding':'10px','borderRadius':'6px','width':'220px'}),
        html.Button('SUBMIT',   id='submit-btn', n_clicks=0,
                    style={'backgroundColor':'#3333aa','color':'white','border':'none',
                           'padding':'10px 24px','borderRadius':'6px','cursor':'pointer','letterSpacing':'2px'}),
        html.Button('NEW GAME', id='reset-btn',  n_clicks=0,
                    style={**S,'border':'1px solid #444','padding':'10px 20px','borderRadius':'6px','cursor':'pointer'}),
    ]),

    dcc.Store(id='game-state', data={'xs':[],'os':[],'past':[],'turn':'X','over':False}),
])

# ── callback ──────────────────────────────────────────────────────────────────

@app.callback(
    Output('board','figure'), Output('status','children'),
    Output('turn-label','children'), Output('coord-input','value'),
    Output('game-state','data'), Output('move-log','children'),
    Input('submit-btn','n_clicks'), Input('reset-btn','n_clicks'),
    State('coord-input','value'), State('mode','value'), State('game-state','data'),
    prevent_initial_call=True,
)
def handle_move(submit_clicks, reset_clicks, raw, mode, state):
    triggered = callback_context.triggered[0]['prop_id']
    xs, os, past, turn = state['xs'], state['os'], state['past'], state['turn']

    def respond(status='', clear=True):
        label = f"Player {state['turn']} — enter your move:"
        return build_figure(xs, os), status, label, ('' if clear else raw), state, build_move_log(xs, os)

    # reset
    if 'reset-btn' in triggered:
        state = {'xs':[],'os':[],'past':[],'turn':'X','over':False}
        return build_figure([],[]), '', 'Player X — enter your move:', '', state, build_move_log([],[])

    # game already over
    if state['over']:
        return respond('Game over! Press NEW GAME to play again.', clear=False)

    # parse and validate input
    try:
        parts = raw.strip().split()
        assert len(parts) == 4
        move = [int(p) for p in parts]
        assert all(0 <= v <= 2 for v in move)
    except:
        return respond('Enter 4 numbers between 0 and 2  (e.g. 0 1 2 1)', clear=False)

    if move in past or move in xs or move in os:
        return respond('That square is already taken!')

    # apply move
    if turn == 'X':
        xs = xs + [move]
    else:
        os = os + [move]
    past = past + [move]

    # check win
    if check_win(xs) or check_win(os):
        winner_name = 'Player X' if check_win(xs) else ('Player O' if mode=='2' else 'Computer')
        state = {'xs':xs,'os':os,'past':past,'turn':turn,'over':True}
        return build_figure(xs, os), f' {winner_name} WINS!', '', '', state, build_move_log(xs, os)

    # computer move (1 player mode)
    if mode == '1' and turn == 'X':
        ai = get_ai_move(xs, os)
        if ai:
            os   = os + [ai]
            past = past + [ai]
            if check_win(os):
                state = {'xs':xs,'os':os,'past':past,'turn':'X','over':True}
                return build_figure(xs, os), ' Computer WINS!', '', '', state, build_move_log(xs, os)

    # next turn
    next_turn = 'O' if (mode=='2' and turn=='X') else 'X'
    state = {'xs':xs,'os':os,'past':past,'turn':next_turn,'over':False}
    return build_figure(xs, os), '', f"Player {next_turn} — enter your move:", '', state, build_move_log(xs, os)

if __name__ == '__main__':
    app.run(debug=False)
