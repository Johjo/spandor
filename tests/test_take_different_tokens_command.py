import dataclasses

from adapters.game_repository_in_memory import GameRepositoryInMemory
from domain.commands.stake_different_tokens_command import TakeDifferentTokensCommand
from domain.domain import Board, Player, Stock

class StockBuilder:
    def build(self):
        return create_stock(quantity=4)


class PlayerBuilder:
    def build(self):
        return Player(stock=create_stock(quantity=0))


class BoardBuilder:
    def __init__(self):
        self.stock = StockBuilder()
        self.players = [PlayerBuilder(), PlayerBuilder()]
        self.number_of_nobles = 3

    def build(self):
        return Board(yellow=0,
                     stock=self.stock.build(),
                     card_level_1=4, card_level_2=4, card_level_3=4, number_of_nobles=self.number_of_nobles,
                     players=[player.build() for player in self.players])


def test_should_first_player_take_token():
    # given
    # i have 0 red, 0 green; 0 black, 0 white, 0 blue
    game = BoardBuilder().build()
    game_repository = GameRepositoryInMemory()
    game_repository.feed(game)
    # when
    # i take 1 red, 1 green; 1 black
    command = TakeDifferentTokensCommand(game_repository=game_repository)
    command.execute(red=True, green=True, black=True, white=False, blue=False)

    # then
    # i have 1 red, 1 green; 1 black, 0 white, 0 blue
    expected = Board(yellow=0,
                     stock=Stock(red=3, green=3, black=3, blue=4, white=4),
                     card_level_1=4,
                     card_level_2=4, card_level_3=4, number_of_nobles=3,
                     players=[Player(Stock(red=1, green=1, black=1, white=0, blue=0)),
                              Player(Stock(red=0, green=0, black=0, white=0, blue=0))])

    actual = game_repository.get_game()
    assert actual == expected


def test_should_first_player_take_token_bis():
    # given
    # i have 0 red, 0 green; 0 black, 0 white, 0 blue
    game = Board(yellow=0,
                 stock=create_stock(quantity=4),
                 card_level_1=4, card_level_2=4, card_level_3=4,
                 number_of_nobles=3,
                 players=[
                     Player(stock=create_stock(quantity=0)),
                     Player(stock=create_stock(quantity=0))])

    game_repository = GameRepositoryInMemory()
    game_repository.feed(game)
    # when
    # i take 1 blue, 1 green; 1 white
    command = TakeDifferentTokensCommand(game_repository=game_repository)
    command.execute(blue=True, green=True, white=True, black=False, red=False)

    # then
    # i have 0 red, 1 green; 0 black, 1 white, 1 blue
    expected = Board(yellow=0,
                     stock=Stock(red=4, green=3, black=4, white=3, blue=3),
                     card_level_1=4,
                     card_level_2=4, card_level_3=4, number_of_nobles=3,
                     players=[Player(Stock(red=0, green=1, black=0, white=1, blue=1)),
                              Player(stock=create_stock(quantity=0))])

    actual = game_repository.get_game()
    assert actual == expected


def create_stock(quantity):
    return Stock(quantity, quantity, quantity, quantity, quantity)
