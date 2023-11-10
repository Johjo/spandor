from dataclasses import dataclass


class GameQuery:
    def query(self):
        return GameNotStartedPresentation()


@dataclass(frozen=True)
class GameNotStartedPresentation:
    pass