from domain.domain import Board, Player, Stock, Card


class StartGameCommand:
    def __init__(self, game_repository):
        self.game_repository = game_repository

    def execute(self, number_of_players):
        if number_of_players == 2:
            number_of_nobles = 3
            initial_color_tokens_quantity = 4
        elif number_of_players == 3:
            number_of_nobles = 4
            initial_color_tokens_quantity = 5
        self.game_repository.save(
            Board(number_of_nobles=number_of_nobles,
                  yellow=5,
                  cards_1=[Card() for _ in range(4)],
                  stock=Stock(**{ color: initial_color_tokens_quantity for color in ["red", "black", "green", "white", "blue"]}),
                  players=[Player(Stock(0, 0, 0, 0, 0)) for _ in range(number_of_players)],
                  card_level_3=4, card_level_2=4, card_level_1=4))