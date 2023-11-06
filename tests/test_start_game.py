import uuid
import pytest

from domain.start_game import Card, TokenStock, Game, GameStartCommand, GameRepository, CardRepository


class StubbedGameRepository(GameRepository):
    def save_game(self, game: Game) -> None:
        self.game = game

    def get_game(self):
        return self.game


GameRepository.register(StubbedGameRepository)


class StubbedCardRepository(CardRepository):
    def __init__(self):
        self.cards = {}

    def feed(self, level, cards):
        self.cards[level] = cards

    def draw_four_cards(self, level):
        return self.cards[level]


class TestWhenStartGame:
    @pytest.fixture
    def card_repository(self, cards_level_1, cards_level_2, cards_level_3) -> CardRepository:
        card_repository: StubbedCardRepository = StubbedCardRepository()
        card_repository.feed(level=1, cards=(cards_level_1))
        card_repository.feed(level=2, cards=(cards_level_2))
        card_repository.feed(level=3, cards=(cards_level_3))
        return card_repository

    @pytest.fixture
    def game_repository(self):
        return StubbedGameRepository()

    @pytest.fixture
    def start_command(self, card_repository, game_repository):
        return GameStartCommand(card_repository=card_repository, game_repository=game_repository)

    def test_then_prepare_a_game_with_some_elements(self, start_command, game_repository,
                                                    cards_level_1, cards_level_2, cards_level_3) -> None:
        start_command.execute(number_of_players=2)

        actual: Game = game_repository.get_game()
        assert actual.cards_level_1 == cards_level_1
        assert actual.cards_level_2 == cards_level_2
        assert actual.cards_level_3 == cards_level_3

    def test_then_prepare_yellow_tokens(self, start_command, game_repository) -> None:
        start_command.execute(number_of_players=2)

        actual: Game = game_repository.get_game()
        assert actual.tokens.yellow == 5

    @pytest.mark.parametrize("number_of_players,expected_tokens", [
        (2, 4),
        (3, 5),
    ])
    def test_then_prepare_tokens_stock_depending_on_number_of_players(self, number_of_players,
                                                                      expected_tokens, start_command,
                                                                      game_repository) -> None:
        start_command.execute(number_of_players=number_of_players)
        actual: Game = game_repository.get_game()
        assert actual.tokens.green == expected_tokens
        assert actual.tokens.red == expected_tokens
        assert actual.tokens.blue == expected_tokens
        assert actual.tokens.black == expected_tokens
        assert actual.tokens.white == expected_tokens


class TestGameRepository():
    def test_should_save_game(self) -> None:
        expected: Game = a_game()
        game_repository: GameRepository = StubbedGameRepository()
        game_repository.save_game(expected)
        actual = game_repository.get_game()
        assert actual == expected


def a_game():
    return Game(
        cards_level_1=many_cards(quantity=4),
        cards_level_2=many_cards(quantity=4),
        cards_level_3=many_cards(quantity=4),
        tokens=TokenStock(yellow=5, green=4, blue=4, white=4, red=4, black=4))


class TestCardRepository():
    @pytest.fixture
    def card_repository(self, cards_level_1, cards_level_2, cards_level_3):
        card_repository = StubbedCardRepository()
        card_repository.feed(level=1, cards=cards_level_1)
        card_repository.feed(level=2, cards=cards_level_2)
        card_repository.feed(level=3, cards=cards_level_3)
        return card_repository

    def test_should_draw_card_of_level_1(self, cards_level_1, card_repository) -> None:
        actual = card_repository.draw_four_cards(level=1)
        assert actual == cards_level_1

    def test_should_draw_card_of_level_2(self, cards_level_2, card_repository) -> None:
        actual = card_repository.draw_four_cards(level=2)
        assert actual == cards_level_2

    def test_should_draw_card_of_level_3(self, cards_level_3, card_repository) -> None:
        actual = card_repository.draw_four_cards(level=3)
        assert actual == cards_level_3


def many_cards(quantity):
    return [Card(id=uuid.uuid4()) for _ in range(quantity)]


@pytest.fixture
def cards_level_1():
    return many_cards(quantity=4)


@pytest.fixture
def cards_level_2():
    return many_cards(quantity=4)


@pytest.fixture
def cards_level_3():
    return many_cards(quantity=4)


def test_fixture(cards_level_1, cards_level_2, cards_level_3):
    assert cards_level_1 != cards_level_2
    assert cards_level_1 != cards_level_3
    assert cards_level_2 != cards_level_3
