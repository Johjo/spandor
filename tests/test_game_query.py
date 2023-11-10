from dataclasses import dataclass

from domain.queries.game_state import GameQuery, GameNotStartedPresentation


@dataclass(frozen=True)
class GamePresentation:
    pass


class TestGameQueryWhenGameIsNotStarted:
    def test_should_get_not_started_presentation(self) -> None:
        actual : GameNotStartedPresentation = GameQuery().query()
        expected : GameNotStartedPresentation = GameNotStartedPresentation()
        assert actual == expected