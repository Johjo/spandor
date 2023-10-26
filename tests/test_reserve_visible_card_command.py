import uuid

from adapters.game_repository_in_memory import GameRepositoryInMemory
from domain.domain import Board
from tests.builder import a_game
from tests.test_start_game import a_card
from tests.test_take_different_tokens_command import a_player


class ReserveVisibleCardCommand:
    def __init__(self, game_repository):
        self.game_repository = game_repository

    def execute(self):
        game : Board = self.game_repository.get_game()

        game.players[0].cards.append(game.cards_1[0])

        self.game_repository.save(game)


def test_():
    # given a game
    game_repository = GameRepositoryInMemory()
    reserved_card = a_card().with_id(uuid.uuid4())
    level_1_cards = [reserved_card, a_card(), a_card(), a_card()]
    game = a_game().starting_for_two_players().with_cards_level_1(level_1_cards)
    game_repository.feed(game.build())

    # when reserve card
    ReserveVisibleCardCommand(game_repository=game_repository).execute()

    # then player have a card
    expected = a_game()\
                    .starting_for_two_players()\
                    .with_cards_level_1(level_1_cards)\
                    .with_players([
                        a_player().with_cards([reserved_card]), a_player()])\
                    .build()
    actual = game_repository.get_game()

    assert actual == expected