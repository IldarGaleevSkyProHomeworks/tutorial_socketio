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
    if not utils.is_data_valid(sid, sio, data):
        print(sid, "sent invalid data")
        return

    player_name = data.get('player_name', None)
    utils.send_registered_message(sid, player_name, sio, playersmanager)
    if len(playersmanager) == 1:
        utils.init_next_player(sio, game, playersmanager)
    print(sid, "registered")


@sio.on("login")
def login(sid, data):
    if not utils.is_data_valid(sid, sio, data):
        print(sid, "sent invalid data")
        return

    personal_key = data.get('pk', None)
    if utils.send_logined_message(sid, personal_key, sio, playersmanager):
        if len(playersmanager) == 1:
            utils.init_next_player(sio, game, playersmanager)
        print(sid, "logined")
    else:
        print(sid, "login failed")


@sio.on("make_turn")
def make_turn(sid, data):
    if not utils.is_data_valid(sid, sio, data):
        print(sid, "sent invalid data")
        return

    word = data.get('word', None)
    utils.check_word(sid, word, sio, game, playersmanager)


@sio.on("who")
def who(sid, data):
    utils.get_active_player(sid, sio, playersmanager)


if __name__ == '__main__':
    try:
        eventlet.wsgi.server(
            eventlet.listen((settings.HOST_NAME, settings.PORT)), app
        )
    except KeyboardInterrupt:
        pass
    print("Server stopped")
