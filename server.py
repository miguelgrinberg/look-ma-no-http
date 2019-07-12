import chess
import socketio
import uvicorn

sio = socketio.AsyncServer()
app = socketio.ASGIApp(sio, static_files={'/': './public/'})
users = {}
games = []


@sio.event
async def connect(sid, environ):
    if len(games) == 0 or games[-1]['black'] is not None:
        game = {
            'white': sid,
            'black': None,
            'board': chess.Board(),
        }
        games.append(game)
        color = 'white'
    else:
        game = games[-1]
        game['black'] = sid
        color = 'black'
    users[sid] = game
    await sio.emit('user_count_changed', len(users))
    await sio.emit('new_game', (game['board'].fen(), color), to=sid)


@sio.event
async def disconnect(sid):
    del users[sid]
    await sio.emit('user_count_changed', len(users))


@sio.event
async def move_made(sid, fromsq, tosq):
    game = users[sid]
    turn = 'white' if game['board'].turn else 'black'
    piece_color = 'white' if game['white'] == sid else 'black'
    if turn == piece_color:
        move = chess.Move.from_uci(fromsq + tosq)
        if move in game['board'].legal_moves:
            game['board'].push(move)
            other_player = game['white'] if piece_color == 'black' \
                else game['black']
            await sio.emit('opponent_move', game['board'].fen(),
                           to=other_player)
    return game['board'].fen()


def main():
    uvicorn.run(app)
