from adapters.game_repository_in_memory import GameRepositoryInMemory
from domain.commands.stake_different_tokens_command import TakeDifferentTokensCommand
from tests.builder import StockBuilder, PlayerBuilder, BoardBuilder

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
