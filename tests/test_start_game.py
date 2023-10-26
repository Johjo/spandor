from adapters.game_repository_in_memory import GameRepositoryInMemory
from domain.commands.start_game_command import StartGameCommand
from domain.domain import Board, Player, Stock
from tests.builder import BoardBuilder


def test_should_start_game_for_two_players():
    game_repository = GameRepositoryInMemory()

    start_game_command = StartGameCommand(game_repository=game_repository)
    start_game_command.execute(number_of_players=2)

    actual = game_repository.get_game()
    expected = BoardBuilder().starting_for_two_players().build()
    assert actual == expected


def test_should_start_game_for_three_players():
    game_repository = GameRepositoryInMemory()

    start_game_command = StartGameCommand(game_repository=game_repository)
    start_game_command.execute(number_of_players=3)

    actual = game_repository.get_game()
    expected = BoardBuilder().starting_for_three_players().build()
    assert actual == expected