from adapters.game_repository_in_memory import GameRepositoryInMemory
from domain.commands.start_game_command import StartGameCommand
from domain.domain import Board, Player, Stock


def test_should_start_game_for_two_players():
    game_repository = GameRepositoryInMemory()

    start_game_command = StartGameCommand(game_repository=game_repository)
    start_game_command.execute(number_of_players=2)


    actual = game_repository.get_game()
    expected = create_board(numberOfNobles=3, initial_quantity_of_tokens=4, number_of_players=2)
    assert actual == expected


def create_board(numberOfNobles, initial_quantity_of_tokens, number_of_players):
    return Board(number_of_nobles=numberOfNobles,
                 yellow=5,
                 stock=Stock(**{color: initial_quantity_of_tokens for color in ["red", "black", "white", "green", "blue"]}),
                 players=[Player(Stock(red=0, green=0, white=0, black=0, blue=0)) for _ in range(number_of_players)],
                 card_level_3=4,
                 card_level_2=4,
                 card_level_1=4)


def test_should_start_game_for_three_players():
    game_repository = GameRepositoryInMemory()

    start_game_command = StartGameCommand(game_repository=game_repository)
    start_game_command.execute(number_of_players=3)


    actual = game_repository.get_game()
    expected = create_board(numberOfNobles=4, initial_quantity_of_tokens=5, number_of_players=3)
    assert actual == expected