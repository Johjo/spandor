import uuid

from django.http import HttpResponse

from python.adapters.game_repository_in_memory import GameRepositoryInMemory
from python.domain.commands_old.start_game_command import StartGameCommand
from python.domain.domain import Card
from python.domain.queries.game_state import GameQuery, GameNotStartedPresentation


def index(request):
    game = GameQuery().query()

    match game:
        case GameNotStartedPresentation():
            return HttpResponse("Do you want to start a game ?")
    return HttpResponse("Hello, world. You're at the polls index.")


class CardRepositoryInMemory:
    def __init__(self):
        self.level_1_cards = [Card(id=uuid.uuid4()) for _ in range(50)]
        self.level_2_cards = [Card(id=uuid.uuid4()) for _ in range(50)]
        self.level_3_cards = [Card(id=uuid.uuid4()) for _ in range(50)]

    def draw_one_card(self, level):
        match level:
            case 1:
                return self.level_1_cards.pop()
            case 2:
                return self.level_2_cards.pop()
            case 3:
                return self.level_3_cards.pop()

    def draw_many(self, level, quantity):
        return [self.draw_one_card(level) for _ in range(quantity)]


def start_game(request):
    game_repository = GameRepositoryInMemory()
    StartGameCommand(game_repository, cards_repository=CardRepositoryInMemory()).execute(number_of_players=2)
    return HttpResponse(str(game_repository.get_game()))
