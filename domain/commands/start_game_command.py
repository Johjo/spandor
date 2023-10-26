from domain.domain import Board, Player, Stock, Card


class StartGameCommand:
    def __init__(self, game_repository, cards_repository):
        self.game_repository = game_repository
        self.cards_repository = cards_repository

    def execute(self, number_of_players):
        if number_of_players == 2:
            number_of_nobles = 3
            initial_color_tokens_quantity = 4
        elif number_of_players == 3:
            number_of_nobles = 4
            initial_color_tokens_quantity = 5
        cards_level_1 = self.cards_repository.draw_many(level=1, quantity=4)
        self.game_repository.save(
            Board(number_of_nobles=number_of_nobles,
                  yellow=5,
                  cards_1=cards_level_1,
                  stock=Stock(**{ color: initial_color_tokens_quantity for color in ["red", "black", "green", "white", "blue"]}),
                  players=[Player(stock=Stock(0, 0, 0, 0, 0), cards=[]) for _ in range(number_of_players)],
                  card_level_3=4, card_level_2=4, card_level_1=4))