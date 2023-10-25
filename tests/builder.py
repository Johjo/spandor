from domain.domain import Stock, Player, Board


class StockBuilder:
    def __init__(self):
        self.red = 0
        self.green = 0
        self.blue = 0
        self.white = 0
        self.black = 0

    def with_same_quantity(self, quantity):
        self.red = self.green = self.blue = self.white = self.black = quantity
        return self

    def with_empty_stock(self):
        self.red = self.green = self.blue = self.white = self.black = 0
        return self

    def build(self):
        return Stock(red=self.red, green=self.green, blue=self.blue, white=self.white, black=self.black)

    def with_stock(self, red, green, black, blue, white):
        self.red = red
        self.green = green
        self.black = black
        self.blue = blue
        self.white = white
        return self


class PlayerBuilder:
    def __init__(self):
        self.stock = StockBuilder().with_empty_stock()

    def build(self):
        return Player(self.stock.build())

    def with_stock(self, stock):
        self.stock = stock
        return self


class BoardBuilder:
    def __init__(self):
        self.starting_for_two_players()

    def starting_for_two_players(self):
        self.stock = StockBuilder().with_same_quantity(quantity=4)
        self.players = [PlayerBuilder(), PlayerBuilder()]
        self.number_of_nobles = 3
        return self

    def build(self):
        return Board(yellow=0,
                     stock=self.stock.build(),
                     card_level_1=4, card_level_2=4, card_level_3=4, number_of_nobles=self.number_of_nobles,
                     players=[player.build() for player in self.players])

    def with_stock(self, stock):
        self.stock = stock
        return self

    def with_players(self, players):
        self.players = players
        return self