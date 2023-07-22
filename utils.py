DEFAULT_USERNAME = "Анонимус"


def init_next_player(sio, game, playersmanager):
    """
    Переключение игрока и отправка сообщения о событии
    :param sio: socketio.Server
    :param game: игра
    :param playersmanager: менеджер игроков
    :return:
    """
    if next_player := playersmanager.get_next_player():

        last_word = game.last_word

        if last_word:
            message = f"Последнее слово \"{game.last_word}\""
        else:
            message = f"Твое слово будет первым!"

        sio.emit(
            event='message',
            to=next_player.sid,
            data={"message": f"Твой ход! {message} присылай событие \"make_turn\" "
                             "с json-объектом: {\"word\":\"твой_ответ\"}"}
        )

        sio.emit(
            event='message',
            data={"message": f"Говорит {next_player.name}, а мы подождем..."},
            skip_sid=next_player.sid
        )


def send_exit_message(sid, sio, playersmanager):
    """
    отправка сообщения об отключении игрока
    :param sio: socketio.Server
    :param game: игра
    :param playersmanager: менеджер игроков
    :return:
    """
    player_info = playersmanager.get_player_name_by_sid(sid)

    if player_info:
        player_name = player_info
    else:
        player_name = DEFAULT_USERNAME

    sio.emit(
        event='message',
        data={"message": f"Игрок {player_name} покинул нас! Press F..."}
    )


def send_hello_message(sid, sio):
    """
    отправка приветствия
    :param sid: id клиента
    :param sio: socketio.Server
    :return:
    """
    sio.emit(
        event='message',
        to=sid,
        data={"message": "Салют! Теперь отправь событие 'register' "
                         "с json-объектом: {\"player_name\": \"Your name\"} "
                         "или 'login' "
                         "с json-объектом: {\"pk\": \"Your_personal_key\"}"})


def send_registered_message(sid, player_name, sio, playersmanager):
    """
    регистрация нового игрока
    :param sid: id клиента
    :param player_name: имя игрока
    :param sio: socketio.Server
    :param playersmanager: менеджер игроков
    :return:
    """
    if player_name:
        pk, _ = playersmanager.register(sid, name=player_name)
        personal_message = f"Дарова, {player_name}, твой ключ доступа: {pk}"
        public_message = f"В наш уютный кружок залетает {player_name}, посмотрим на что он способен!"
    else:
        personal_message = "Моя твоя не понимать... ты чего мне прислал?"
        public_message = None

    sio.emit(
        event='message',
        to=sid,
        data={"message": personal_message}
    )

    if public_message:
        sio.emit(
            event='message',
            data={"message": public_message},
            skip_sid=sid
        )


def send_logined_message(sid, personal_key, sio, playersmanager) -> bool:
    """
    регистрация нового игрока
    :param sid: id клиента
    :param personal_key: персональный ключ игрока
    :param sio: socketio.Server
    :param playersmanager: менеджер игроков
    :return:
    """
    is_logined = False
    public_message = None

    if personal_key:
        _, player = playersmanager.register(sid, pk=personal_key)
    else:
        player = None
        personal_message = "Моя твоя не понимать... ты чего мне прислал?"

    if player:
        personal_message = f"С возвращением, {player.name}"
        public_message = f"К нам вернулся {player.name}!"
        is_logined = True
    else:
        personal_message = "Нет у меня такого ключа... падазрительна, ты чего задумал!? 😑"

    sio.emit(
        event='message',
        to=sid,
        data={"message": personal_message}
    )

    if public_message:
        sio.emit(
            event='message',
            data={"message": public_message},
            skip_sid=sid
        )

    return is_logined


def check_word(sid, word, sio, game, playersmanager):
    """
    проверка слова
    :param sid: id клиента
    :param word: проверяемое слово
    :param sio: socketio.Server
    :param game: игра
    :param playersmanager: менеджер игроков
    :return:
    """
    if playersmanager.is_current_player(sid):

        player_name = playersmanager.get_player_name_by_sid(sid)
        is_correct = False

        if not word or len(word) < 2 or not word.isalpha():
            personal_message = "Штааа!? Я тебя не понял, давай заново и нормальными словами.."
            public_message = f"{player_name} втирает нам какую-то дичь, послушаем его еще раз."
        elif game.test_word(word):
            personal_message = "Красава!"
            public_message = f"{player_name} ответил \"{word}\", ответ засчитан"
            is_correct = True
        else:
            personal_message = f"Не-не... так не пойдет! Предыдущее слово было \"{game.last_word}\", давай заново.."
            public_message = f"{player_name} ответил \"{word}\", послушаем его еще раз."

        sio.emit(
            event='message',
            to=sid,
            data={"message": personal_message}
        )

        sio.emit(
            event='message',
            data={"message": public_message},
            skip_sid=sid
        )

        if is_correct:
            init_next_player(sio, game, playersmanager)
    else:
        noname_message = ""
        if not playersmanager.get_player_name_by_sid(sid):
            noname_message = " И вообще, для начала представься"
        sio.emit(
            event='message',
            to=sid,
            data={"message": f"Акстись! Сейчас не твой ход!{noname_message}"}
        )


def get_active_player(sid, sio, playersmanager):
    """
    запрос активного игрока
    :param sid: id клиента
    :param sio: socketio.Server
    :param playersmanager: менеджер игроков
    :return:
    """
    if curr_player_name := playersmanager.get_current_player_name():
        message = f"Сейчас все ждут \"{curr_player_name}\""
    else:
        message = "Хммм... ничего не знаю, отстань.."

    sio.emit(
        event='message',
        to=sid,
        data={"message": message}
    )


def is_data_valid(sid, sio, data) -> bool:
    if type(data) is not dict:
        sio.emit(
            event='message',
            to=sid,
            data={"message": "Прекрати слать мне ерунду! Присылай JSON- тогда поговорим..."}
        )
        return False
    return True
