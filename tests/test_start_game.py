import uuid

from adapters.game_repository_in_memory import GameRepositoryInMemory
from domain.commands.start_game_command import StartGameCommand
from domain.domain import Board, Player, Stock
from tests.builder import BoardBuilder, CardBuilder


class CardRepositoryInMemory:
    def feed_level_1_cards(self, cards):
        self.cards_1 = [card.build() for card in cards]


def test_should_start_game_for_two_players():
    game_repository = GameRepositoryInMemory()
    cards_repository = CardRepositoryInMemory()

    level_1_cards = [CardBuilder().with_id(uuid.uuid4()) for _ in range(4)]
    cards_repository.feed_level_1_cards(level_1_cards)

    start_game_command = StartGameCommand(game_repository=game_repository)
    start_game_command.execute(number_of_players=2)

    actual = game_repository.get_game()
    expected = BoardBuilder()\
                    .starting_for_two_players()\
                    .with_cards_level_1(cards=level_1_cards)\
                    .build()
    assert actual == expected


def test_should_start_game_for_three_players():
    game_repository = GameRepositoryInMemory()

    start_game_command = StartGameCommand(game_repository=game_repository)
    start_game_command.execute(number_of_players=3)

    actual = game_repository.get_game()
    expected = BoardBuilder()\
                    .starting_for_three_players()\
                    .with_cards_level_1(cards=[CardBuilder() for _ in range(4)])\
                    .build()

    assert actual == expected