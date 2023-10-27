import uuid

from adapters.game_repository_in_memory import GameRepositoryInMemory
from domain.domain import Board
from tests.builder import a_game
from tests.test_start_game import a_card, CardRepositoryStubbed
from tests.test_take_different_tokens_command import a_player


class ReserveVisibleCardCommand:
    def __init__(self, game_repository, card_repository):
        self.game_repository = game_repository
        self.card_repository = card_repository

    def execute(self):
        game : Board = self.game_repository.get_game()

        game.players[0].cards.append(game.cards_1[0])
        game.cards_1[0] = self.card_repository.draw_one_card(level=1)
        self.game_repository.save(game)


def test_():
    # given a game
    game_repository = GameRepositoryInMemory()
    reserved_card = a_card()
    new_card = a_card()
    level_1_cards = [reserved_card, a_card(), a_card(), a_card()]
    game = a_game().starting_for_two_players().with_cards_level_1(level_1_cards)
    game_repository.feed(game.build())

    card_repository = CardRepositoryStubbed()
    card_repository.feed(level=1, quantity=1, cards=[new_card])

    # when reserve card
    ReserveVisibleCardCommand(game_repository=game_repository, card_repository=card_repository).execute()

    # then player have a card
    expected = a_game()\
                    .starting_for_two_players()\
                    .with_cards_level_1([new_card, level_1_cards[1], level_1_cards[2], level_1_cards[3]])\
                    .with_players([
                        a_player().with_cards([reserved_card]), a_player()])\
                    .build()
    actual = game_repository.get_game()

    assert actual == expected