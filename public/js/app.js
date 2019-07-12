var sio = io();
var game = new Chess();
var board = new ChessBoard('board', {
    position: game.fen(),
    draggable: true,
    onDrop: function(from, to) {
        if (game.turn() != piece_color[0]) {
            return 'snapback';
        }
        var move = game.move({from: from, to: to});
        if (!move) {
            return 'snapback';
        }
        sio.emit('move_made', from, to, function(fen) {
            updateBoard(fen);
        });
    },
});
var piece_color;
var watch = false;
var all_games = {};

$('#watch').click(function() {
    watch = !watch;
    if (watch) {
        sio.emit('start_watching');
    }
    else {
        sio.emit('stop_watching');
    }
});

function updateBoard(fen) {
    game.load(fen);
    board.position(game.fen());
}

sio.on('user_count_changed', function(new_count) {
    $('#user_count').text(new_count);
});

sio.on('new_game', function(fen, color) {
    updateBoard(fen);
    board.orientation(color);
    piece_color = color;
});

sio.on('opponent_move', function(fen) {
    updateBoard(fen);
});

sio.on('game_updates', function(updates) {
    Object.keys(updates).forEach(function(id) {
        if (!(id in all_games)) {
            $('#watched_games').append(
                '<div id="' + id + '" class="watched_board"></div>');
            all_games[id] = new ChessBoard(id);
        }
        all_games[id].position(updates[id]);
    });
});
