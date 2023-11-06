import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass


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


class CardRepository(ABC):
    @abstractmethod
    def draw_four_cards(self, level):
        pass