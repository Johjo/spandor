from abc import ABC, abstractmethod
from dataclasses import dataclass

import pytest


@dataclass(frozen=True)
class Stock:
    red: int
    green: int
    blue: int
    white: int
    black: int

    def increase(self, color):
        quantities = self.__dict__
        quantities[color] += 1
        return Stock(**quantities)

    def decrease(self, color):
        quantities = self.__dict__
        quantities[color] -= 1
        return Stock(**quantities)


@dataclass(frozen=True)
class Player:
    stock: Stock


@dataclass(frozen=True)
class Game:
    player: Player
    stock: Stock


class GameRepository(ABC):
    @abstractmethod
    def get_game(self) -> Game:
        pass

    @abstractmethod
    def save(self, game: Game):
        pass


class StubbedGameRepository(GameRepository):
    def get_game(self):
        return self.game

    def feed(self, game: Game):
        self.game = game

    def save(self, game) -> None:
        self.game = game


class TakeDifferentTokenCommand:
    def __init__(self, game_repository: GameRepository):
        self.game_repository = game_repository

    def execute(self, red: bool = False, blue: bool = False, black: bool = False, green: bool = False,
                white: bool = False) -> None:

        game: Game = self.game_repository.get_game()
        game = self._take_tokens(game, black, blue, green, red, white)
        self.game_repository.save(game)

    def _take_tokens(self, game, black, blue, green, red, white):
        (game_stock, player_stock) = game.stock, game.player.stock

        tokens = [("red", red), ("blue", blue), ("green", green), ("black", black), ("white", white)]
        for (color, taken) in tokens:
            if taken:
                player_stock = player_stock.increase(color)
                game_stock = game_stock.decrease(color)
        return Game(player=Player(player_stock), stock=game_stock)


class TestWhenTakeDifferentTokens:
    @pytest.mark.parametrize("taken, expected", [
        ({"red": True, "blue": True, "black": True}, Stock(red=1, blue=1, black=1, white=0, green=0)),
        ({"red": True, "green": True, "white": True}, Stock(red=1, blue=0, black=0, white=1, green=1)),
        ({"blue": True, "green": True, "white": True}, Stock(red=0, blue=1, black=0, white=1, green=1)),
    ])
    def test_then_increase_player_stock(self, taken, expected):
        game_repository = StubbedGameRepository()
        game_repository.feed(
            Game(player=Player(Stock(red=0, blue=0, black=0, white=0, green=0)), stock=Stock(0, 0, 0, 0, 0, )))

        TakeDifferentTokenCommand(game_repository=game_repository).execute(**taken)

        actual = game_repository.get_game()
        assert actual.player.stock == expected

    @pytest.mark.parametrize("taken, expected", [
        ({"red": True, "blue": True, "black": True}, Stock(red=2, blue=2, black=2, white=1, green=1)),
        ({"red": True, "green": True, "white": True}, Stock(red=2, blue=1, black=1, white=2, green=2)),
        ({"blue": True, "green": True, "white": True}, Stock(red=1, blue=2, black=1, white=2, green=2)),
    ])
    def test_then_cumulate_player_tokens(self, taken, expected):
        game_repository = StubbedGameRepository()
        game_repository.feed(
            Game(player=Player(Stock(red=1, blue=1, black=1, white=1, green=1)), stock=Stock(0, 0, 0, 0, 0, )))

        TakeDifferentTokenCommand(game_repository=game_repository).execute(**taken)

        actual = game_repository.get_game()
        assert actual.player.stock == expected

    @pytest.mark.parametrize("stock,taken,expected", [
        (Stock(red=4, blue=4, black=4, green=4, white=4), {"red": True, "blue": True, "black": True},
         Stock(red=3, blue=3, black=3, green=4, white=4)),
        (Stock(red=4, blue=4, black=4, green=4, white=4), {"black": True, "white": True, "green": True},
         Stock(red=4, blue=4, black=3, green=3, white=3)),
        (Stock(red=3, blue=3, black=3, green=3, white=3), {"black": True, "white": True, "green": True},
         Stock(red=3, blue=3, black=2, green=2, white=2)),
    ])
    def test_then_decrease_stock(self, stock, taken, expected) -> None:
        game_repository = StubbedGameRepository()
        game_repository.feed(
            Game(player=Player(Stock(red=1, blue=1, black=1, white=1, green=1)), stock=stock))

        TakeDifferentTokenCommand(game_repository=game_repository).execute(**taken)

        actual = game_repository.get_game()
        assert actual.stock == expected


