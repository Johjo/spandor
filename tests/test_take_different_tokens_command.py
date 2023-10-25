import dataclasses

from adapters.game_repository_in_memory import GameRepositoryInMemory
from domain.commands.stake_different_tokens_command import TakeDifferentTokensCommand
from domain.domain import Board, Player, Stock

class StockBuilder:
    def __init__(self):
        self.red = 0
        self.green = 0
        self.blue = 0
        self.white = 0
        self.black = 0

    def with_same_quantity(self, quantity):
        self.red = self.green = self.blue = self.white = self.black = quantity
        return self

    def with_empty_stock(self):
        self.red = self.green = self.blue = self.white = self.black = 0
        return self

    def build(self):
        return Stock(red=self.red, green=self.green, blue=self.blue, white=self.white, black=self.black)

    def with_stock(self, red, green, black, blue, white):
        self.red = red
        self.green = green
        self.black = black
        self.blue = blue
        self.white = white
        return self


class PlayerBuilder:
    def __init__(self):
        self.stock = StockBuilder().with_empty_stock()

    def build(self):
        return Player(self.stock.build())

    def with_stock(self, stock):
        self.stock = stock
        return self


class BoardBuilder:
    def __init__(self):
        self.starting_for_two_players()

    def starting_for_two_players(self):
        self.stock = StockBuilder().with_same_quantity(quantity=4)
        self.players = [PlayerBuilder(), PlayerBuilder()]
        self.number_of_nobles = 3
        return self

    def build(self):
        return Board(yellow=0,
                     stock=self.stock.build(),
                     card_level_1=4, card_level_2=4, card_level_3=4, number_of_nobles=self.number_of_nobles,
                     players=[player.build() for player in self.players])

    def with_stock(self, stock):
        self.stock = stock
        return self

    def with_players(self, players):
        self.players = players
        return self


def a_stock(red, green, black, blue, white):
    return StockBuilder().with_stock(red=red, green=green, black=black, blue=blue, white = white)


def a_player():
    return PlayerBuilder()


def a_game():
    return BoardBuilder()


def test_should_first_player_take_token():
    # given
    # i have 0 red, 0 green; 0 black, 0 white, 0 blue
    game_repository = GameRepositoryInMemory()
    game_repository.feed(a_game().starting_for_two_players().build())

    # when
    # i take 1 red, 1 green; 1 black
    command = TakeDifferentTokensCommand(game_repository=game_repository)
    command.execute(red=True, green=True, black=True, white=False, blue=False)

    # then
    # i have 1 red, 1 green; 1 black, 0 white, 0 blue
    expected = a_game()\
                   .with_stock(a_stock(red=3, green=3, black=3, blue=4, white=4))\
                   .with_players([
                        a_player().with_stock(a_stock(red=1, green=1, black=1, white=0, blue=0)),
                        a_player()]).build()

    actual = game_repository.get_game()
    assert actual == expected


def test_should_first_player_take_token_bis():
    # given
    # i have 0 red, 0 green; 0 black, 0 white, 0 blue
    game_repository = GameRepositoryInMemory()
    game_repository.feed(a_game().starting_for_two_players().build())
    # when
    # i take 1 blue, 1 green; 1 white
    command = TakeDifferentTokensCommand(game_repository=game_repository)
    command.execute(blue=True, green=True, white=True, black=False, red=False)

    # then
    # i have 0 red, 1 green; 0 black, 1 white, 1 blue
    expected = a_game()\
        .with_stock(a_stock(red=4, green=3, black=4, white=3, blue=3))\
        .with_players([
            a_player().with_stock(a_stock(red=0, green=1, black=0, white=1, blue=1)),
            a_player()])\
        .build()

    actual = game_repository.get_game()
    assert actual == expected
