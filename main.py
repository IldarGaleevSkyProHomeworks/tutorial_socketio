import eventlet
import socketio

import settings
import game
import playersmanager
import utils

playersmanager = playersmanager.PlayersManager()
game = game.Game("ъь")
sio = socketio.Server()
app = socketio.WSGIApp(sio)


@sio.event
def connect(sid, environ):
    utils.send_hello_message(sid, sio)
    print(sid, "connected")


@sio.event
def disconnect(sid):
    utils.send_exit_message(sid, sio, playersmanager)
    if playersmanager.is_current_player(sid):
        utils.init_next_player(sio, game, playersmanager)
    playersmanager.logout(sid)

    print(sid, "disconnected")


@sio.on("register")
def register(sid, data):
    player_name = data.get('player_name', None)
    utils.send_registered_message(sid, player_name, sio, playersmanager)
    if len(playersmanager) == 1:
        utils.init_next_player(sio, game, playersmanager)
    print(sid, "registered")


@sio.on("make_turn")
def make_turn(sid, data):
    word = data.get('word', None)
    utils.check_word(sid, word, sio, game, playersmanager)


@sio.on("who")
def make_turn(sid, data):
    utils.get_active_player(sid, sio, playersmanager)


if __name__ == '__main__':
    try:
        eventlet.wsgi.server(
            eventlet.listen((settings.HOST_NAME, settings.PORT)), app
        )
    except KeyboardInterrupt:
        pass
    print("Server stopped")
