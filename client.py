import chess
import socketio

sio = socketio.Client()
board = chess.Board()
piece_color = None


def move_if_turn():
    turn = 'white' if board.turn else 'black'
    if piece_color == turn:
        print(board)
        print('you play', piece_color)
        print('your move:')
        move = input()
        fen = sio.call('move_made', (move[:2], move[2:]))
        board.set_fen(fen)
        move_if_turn()


@sio.event
def user_count_changed(new_count):
    print(new_count, 'users online')


@sio.event
def new_game(fen, color):
    board.set_fen(fen)
    global piece_color
    piece_color = color
    move_if_turn()


@sio.event
def opponent_move(fen):
    board.set_fen(fen)
    move_if_turn()


def main():
    sio.connect('http://localhost:8000')
    sio.wait()


main()
