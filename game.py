class Game:
    """
    Объект, представляющий игру в "Города"
    """

    def __init__(self, impossible_chars: str = None):
        self._last_word = None
        self._impossible_chars = impossible_chars.lower() if impossible_chars else []

    def test_word(self, word: str) -> bool:
        """
        Проверка слова на правильность
        :param word: проверяемое слово (не чувствительно к регистру)
        :return:
        """

        if not word:
            raise ValueError("Word is empty")

        word = word.lower()

        if not self._last_word:
            self._last_word = word
            return True

        last_char = self._last_word[-1]
        if last_char in self._impossible_chars:
            last_char = self._last_word[-2]
        result = last_char == word[0]

        if result:
            self._last_word = word

        return result

    @property
    def last_word(self) -> str | None:
        """
        Последнее загаданное слово
        :return:
        """
        return self._last_word


def _test():
    game = Game()

    assert game.test_word("word")
    assert not game.test_word("word")
    assert game.test_word("dwarf")
    assert game.test_word("Film")


if __name__ == '__main__':
    _test()
