from abc import ABC, abstractmethod
from dataclasses import dataclass


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