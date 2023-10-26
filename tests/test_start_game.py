import uuid

from adapters.game_repository_in_memory import GameRepositoryInMemory
from domain.commands.start_game_command import StartGameCommand
from domain.domain import Board, Player, Stock
from tests.builder import BoardBuilder, CardBuilder


class CardRepositoryStubbed:
    def __init__(self):
        self.cards = {}

    def feed(self, level, quantity, cards):
        self.cards[(level, quantity)] = [card.build() for card in cards]

    def draw_many(self, level, quantity):
        return self.cards[(level, quantity)]

def test_should_start_game_for_two_players():
    game_repository = GameRepositoryInMemory()
    cards_repository = CardRepositoryStubbed()

    level_1_cards = [CardBuilder().with_id(uuid.uuid4()) for _ in range(4)]
    cards_repository.feed(level=1, quantity=4, cards=level_1_cards)

    start_game_command = StartGameCommand(game_repository=game_repository, cards_repository=cards_repository)
    start_game_command.execute(number_of_players=2)

    actual = game_repository.get_game()
    expected = BoardBuilder()\
                    .starting_for_two_players()\
                    .with_cards_level_1(cards=level_1_cards)\
                    .build()
    assert actual == expected


def test_should_start_game_for_three_players():
    game_repository = GameRepositoryInMemory()
    cards_repository = CardRepositoryStubbed()

    level_1_cards = [CardBuilder().with_id(uuid.uuid4()) for _ in range(4)]
    cards_repository.feed(level=1, quantity=4, cards=level_1_cards)

    start_game_command = StartGameCommand(game_repository=game_repository, cards_repository=cards_repository)
    start_game_command.execute(number_of_players=3)

    actual = game_repository.get_game()
    expected = BoardBuilder()\
                    .starting_for_three_players()\
                    .with_cards_level_1(cards=level_1_cards)\
                    .build()
    assert actual == expected
