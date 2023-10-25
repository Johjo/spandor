import copy


class GameRepositoryInMemory:
    def get_game(self):
        return copy.deepcopy(self.game)

    def save(self, game):
        self.game = game

    def feed(self, game):
        self.game = game