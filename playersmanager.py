import random


class Player:
    def __init__(self, player_name=None):
        self._sid = None
        self._player_name = player_name

    @property
    def name(self):
        return self._player_name

    @name.setter
    def name(self, value):
        self._player_name = value

    @property
    def sid(self):
        return self._sid

    @sid.setter
    def sid(self, value):
        self._sid = value


class PlayersManager:
    """
    Менеджер игроков
    """

    __PK_SEED = "0123456789AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz"

    def __init__(self):
        self.__fake_db = {}
        self._active_players_list = {}
        self._last_player = None

    def __db_get_player_by_pk(self, pk) -> Player | None:
        if not pk:
            raise ValueError("Invalid personal key")
        return self.__fake_db.get(pk, None)

    def __db_get_player_by_sid(self, sid) -> Player | None:
        if not sid:
            raise ValueError("Invalid personal key")

        found_player = [player for _, player in self.__fake_db.items() if player.sid == sid]

        if found_player:
            return found_player[0]
        else:
            return None

    def __db_get_pk_by_sid(self, sid) -> str | None:
        pk_list = [pk for pk, player in self.__fake_db.items() if player.sid == sid]
        if pk_list:
            return pk_list[0]
        return None

    def __db_get_unique_pk(self):
        while True:
            new_pk = ''.join(random.sample(PlayersManager.__PK_SEED, 6))
            if new_pk in self.__fake_db:
                continue
            return new_pk

    def __db_create_player(self, name):
        if not name:
            raise ValueError("Invalid sid or name")
        player_pk = self.__db_get_unique_pk()
        new_player = Player(name)
        self.__fake_db[player_pk] = new_player

        return player_pk, new_player

    def register(self, sid, name=None, pk=None) -> tuple[None, None] | tuple[str, Player]:
        """
        Регистрация игрока
        :param sid: id
        :param name: Имя
        :param pk: personal key
        :return: personal key and Player instance
        """
        if not sid:
            raise ValueError("Invalid SID")

        if pk:
            if not (player := self.__db_get_player_by_pk(pk)):
                return None, None
        elif name:
            pk, player = self.__db_create_player(name)
        else:
            raise ValueError("Invalid args")

        player.sid = sid
        self._active_players_list[sid] = player
        return pk, player

    def logout(self, sid):
        """
        Удаление игрока
        :param sid: id
        :return:
        """
        if sid in self._active_players_list:
            del self._active_players_list[sid]

        if not self._active_players_list or self._last_player == sid:
            self._last_player = None

    def get_next_player(self) -> Player | None:
        """
        Получить следующего игрока
        :return: id и Имя игрока либо None если не удалось найти игроков
        """
        if not self._active_players_list:
            return None

        sids = list(self._active_players_list.keys())

        if self._last_player is None or self._last_player == sids[-1]:
            self._last_player = sids[0]
        else:
            next_player_index = sids.index(self._last_player) + 1
            if next_player_index > len(self._active_players_list):
                return None
            self._last_player = sids[next_player_index]

        return self.__db_get_player_by_sid(self._last_player)

    def is_current_player(self, sid):
        """
        Проверка активного игрока по id
        :param sid:
        :return:
        """
        return sid == self._last_player

    def get_current_player_name(self) -> str | None:
        """
        Получить имя активного игрока
        :return:
        """
        if self._last_player:
            curr_player = self.__db_get_player_by_sid(self._last_player)
            if curr_player:
                return curr_player.name
        return None

    def get_player_name_by_sid(self, sid):
        """
        Получить имя игрока по id
        :param sid: id игрока
        :return:
        """
        curr_player = self.__db_get_player_by_sid(sid)
        if curr_player:
            return curr_player.name
        return None

    def get_pk_by_sid(self, sid):
        return self.__db_get_pk_by_sid(sid)

    def __len__(self):
        return len(self._active_players_list)


def _test():
    playersmanager = PlayersManager()

    playersmanager.register(1, 'Player 1')
    playersmanager.register(2, 'Player 2')
    player3_pk, player3_instance = playersmanager.register(3, 'Player 3')

    assert playersmanager.get_next_player().name == "Player 1"
    assert playersmanager.get_next_player().name == "Player 2"
    assert playersmanager.get_next_player().name == "Player 3"
    assert playersmanager.get_next_player().name == "Player 1"
    assert playersmanager.is_current_player(1)
    assert not playersmanager.is_current_player(2)

    playersmanager.logout(3)

    _, relogined_player3 = playersmanager.register(333, pk=player3_pk)

    assert relogined_player3 is player3_instance
    assert relogined_player3.sid == 333
    assert playersmanager.get_player_name_by_sid(333) == "Player 3"

    print("Test OK")


if __name__ == '__main__':
    _test()
