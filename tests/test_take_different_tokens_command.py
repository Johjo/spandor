import pytest

from adapters.game_repository_in_memory import GameRepositoryInMemory
from domain.commands.stake_different_tokens_command import TakeDifferentTokensCommand, TooManyTokensTakenException
from tests.builder import StockBuilder, PlayerBuilder, BoardBuilder

def a_stock(red, green, black, blue, white):
    return StockBuilder().with_stock(red=red, green=green, black=black, blue=blue, white=white)


def a_player():
    return PlayerBuilder()


def a_game():
    return BoardBuilder()


@pytest.mark.parametrize("tokens,expected",
[
    ({"red":True, "green":True, "black":True, "white":False, "blue":False},
        a_game() \
            .with_stock(a_stock(red=3, green=3, black=3, blue=4, white=4)) \
            .with_players([
                a_player().with_stock(a_stock(red=1, green=1, black=1, white=0, blue=0)),
                a_player()])),

        ({"red":False, "green":True, "black":False, "white":True, "blue":True},
        a_game() \
            .with_stock(a_stock(red=4, green=3, black=4, blue=3, white=3)) \
            .with_players([
                a_player().with_stock(a_stock(red=0, green=1, black=0, white=1, blue=1)),
                a_player()])),
])
def test_should_first_player_take_token(tokens, expected):
    # given
    game_repository = GameRepositoryInMemory()
    game_repository.feed(a_game().starting_for_two_players().build())

    # when
    command = TakeDifferentTokensCommand(game_repository=game_repository)
    command.execute(**tokens)

    # then
    actual = game_repository.get_game()
    assert actual == expected.build()


def test_should_tell_when_take_too_many_tokens():
    # given
    game_repository = GameRepositoryInMemory()
    game_repository.feed(a_game().starting_for_two_players().build())

    # when / then
    with pytest.raises(TooManyTokensTakenException):
        command = TakeDifferentTokensCommand(game_repository=game_repository)
        command.execute(red=True, green=True, black=True, white=True, blue=False)
