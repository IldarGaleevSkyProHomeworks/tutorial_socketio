from collections import namedtuple

Player = namedtuple('Player', ['sid', 'name'])


class PlayersManager:
    """
    Менеджер игроков
    """

    def __init__(self):
        self._players_list = {}
        self._last_player = None

    def register(self, sid, name):
        """
        Регистрация игрока
        :param sid: id
        :param name: Имя
        :return:
        """
        self._players_list[sid] = name

    def logout(self, sid):
        """
        Удаление игрока
        :param sid: id
        :return:
        """
        if sid in self._players_list:
            del self._players_list[sid]

        if not self._players_list:
            self._last_player = None

    def get_next_player(self) -> Player | None:
        """
        Получить следующего игрока
        :return: id и Имя игрока либо None если не удалось найти игроков
        """
        if not self._players_list:
            return None

        sids = list(self._players_list.keys())

        if self._last_player is None or self._last_player == sids[-1]:
            self._last_player = sids[0]
        else:
            next_player_index = sids.index(self._last_player) + 1
            if next_player_index > len(self._players_list):
                return None
            self._last_player = sids[next_player_index]

        return Player(sid=self._last_player, name=self._players_list[self._last_player])

    def is_current_player(self, sid):
        """
        Проверка активного игрока по id
        :param sid:
        :return:
        """
        return sid == self._last_player

    def get_current_player_name(self):
        """
        Получить имя активного игрока
        :return:
        """
        if self._last_player:
            return self._players_list[self._last_player]

    def get_player_name_by_sid(self, sid):
        """
        Получить имя игрока по id
        :param sid: id игрока
        :return:
        """
        if sid in self._players_list:
            return self._players_list[sid]
        return None

    def __len__(self):
        return len(self._players_list)


def _test():
    playersmanager = PlayersManager()

    playersmanager.register(1, 'Player 1')
    playersmanager.register(2, 'Player 2')
    playersmanager.register(3, 'Player 3')

    assert playersmanager.get_next_player().name == "Player 1"
    assert playersmanager.get_next_player().name == "Player 2"
    assert playersmanager.get_next_player().name == "Player 3"
    assert playersmanager.get_next_player().name == "Player 1"
    assert playersmanager.is_current_player(1)
    assert not playersmanager.is_current_player(2)


if __name__ == '__main__':
    _test()
