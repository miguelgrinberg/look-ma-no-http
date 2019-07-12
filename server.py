import uuid
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
            'id': uuid.uuid4().hex,
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
    await sio.emit('game_updates', {game['id']: game['board'].fen()},
                   to='watchers')


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
            await sio.emit('game_updates', {game['id']: game['board'].fen()},
                           to='watchers')
    return game['board'].fen()


@sio.event
async def start_watching(sid):
    sio.enter_room(sid, 'watchers')
    await sio.emit('game_updates', {game['id']: game['board'].fen()
                                    for game in games}, to=sid)


@sio.event
def stop_watching(sid):
    sio.leave_room(sid, 'watchers')


def main():
    uvicorn.run(app)
