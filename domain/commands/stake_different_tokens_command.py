class TakeDifferentTokensCommand:
    def __init__(self, game_repository):
        self.game_repository = game_repository

    def execute(self, blue, green, red, black, white):
        board = self.game_repository.get_game()
        player = board.players[0]
        quantity = 0

        tokens = [("red", red), ("blue", blue), ("green", green), ("black", black), ("white", white) ]

        for (color, taken) in tokens:
            if taken:
                board.stock.decrease(color, quantity=1)
                player.stock.increase(color, quantity=1)
                quantity += 1

        if quantity == 4:
            raise TooManyTokensTakenException()

        self.game_repository.save(board)


class TooManyTokensTakenException(Exception):
    pass