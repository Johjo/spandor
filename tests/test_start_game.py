import uuid
import pytest
from adapters.game_repository_in_memory import GameRepositoryInMemory
from domain.commands.start_game_command import StartGameCommand
from tests.builder import CardBuilder, a_game


class CardRepositoryStubbed:
    def __init__(self):
        self.cards = {}

    def feed(self, level, quantity, cards):
        self.cards[(level, quantity)] = [card.build() for card in cards]

    def draw_many(self, level, quantity):
        return self.cards[(level, quantity)]

@pytest.mark.parametrize("number_of_players,expected", [
    (2, a_game().starting_for_two_players()),
    (3, a_game().starting_for_three_players()),
])
def test_should_start_game(number_of_players, expected):
    game_repository = GameRepositoryInMemory()
    cards_repository = CardRepositoryStubbed()

    level_1_cards = [a_card().with_id(uuid.uuid4()) for _ in range(4)]
    cards_repository.feed(level=1, quantity=4, cards=level_1_cards)

    start_game_command = StartGameCommand(game_repository=game_repository, cards_repository=cards_repository)
    start_game_command.execute(number_of_players=number_of_players)

    actual = game_repository.get_game()
    expected = expected.with_cards_level_1(cards=level_1_cards).build()
    assert actual == expected


def a_card():
    return CardBuilder()
