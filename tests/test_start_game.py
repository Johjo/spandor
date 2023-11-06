import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass

import pytest


@dataclass
class Card:
    id: uuid.UUID


@dataclass
class TokenStock:
    yellow: int
    green: int
    red: int
    blue: int
    black: int
    white: int


@dataclass
class Game:
    cards_level_1: list[Card]
    cards_level_2: list[Card]
    cards_level_3: list[Card]
    tokens: TokenStock


class GameStartCommand:
    def __init__(self, game_repository, card_repository):
        self.card_repository = card_repository
        self.game_repository = game_repository

    def execute(self, number_of_players):
        initial_tokens_quantity = 4 if number_of_players == 2 else 5

        self.game_repository.save_game(Game(
            cards_level_1=self.card_repository.draw_four_cards(level=1),
            cards_level_2=self.card_repository.draw_four_cards(level=2),
            cards_level_3=self.card_repository.draw_four_cards(level=3),
            tokens=TokenStock(yellow=5, green=initial_tokens_quantity, blue=initial_tokens_quantity,
                              white=initial_tokens_quantity, red=initial_tokens_quantity,
                              black=initial_tokens_quantity)))


class GameRepository(ABC):
    @abstractmethod
    def get_game(self):
        pass

    @abstractmethod
    def save_game(self, game: Game) -> None:
        pass


class StubbedGameRepository(GameRepository):
    def save_game(self, game: Game) -> None:
        self.game = game

    def get_game(self):
        return self.game


GameRepository.register(StubbedGameRepository)


class CardRepository(ABC):
    @abstractmethod
    def draw_four_cards(self, level):
        pass


class StubbedCardRepository(CardRepository):
    def __init__(self):
        self.cards = {}

    def feed(self, level, cards):
        self.cards[level] = cards

    def draw_four_cards(self, level):
        return self.cards[level]


class TestStartGameCommand:
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

    def test_should_start_a_game_with_some_elements(self, start_command, game_repository,
                                                    cards_level_1, cards_level_2, cards_level_3) -> None:
        start_command.execute(number_of_players=2)

        actual: Game = game_repository.get_game()
        assert actual.cards_level_1 == cards_level_1
        assert actual.cards_level_2 == cards_level_2
        assert actual.cards_level_3 == cards_level_3

    def test_should_start_a_game_with_five_yellow_tokens(self, start_command, game_repository):
        start_command.execute(number_of_players=2)

        actual: Game = game_repository.get_game()
        assert actual.tokens.yellow == 5

    @pytest.mark.parametrize("number_of_players,expected_tokens", [
        (2, 4),
        (3, 5),
    ])
    def test_should_start_a_game_with_tokens_stock_depending_on_number_of_players(self, number_of_players,
                                                                                  expected_tokens, start_command,
                                                                                  game_repository):
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
