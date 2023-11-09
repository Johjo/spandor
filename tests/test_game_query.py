from dataclasses import dataclass


@dataclass(frozen=True)
class GamePresentation:
    pass


def test_should_get_game() -> None:
    actual : GamePresentation = GamePresentation()
    expected : GamePresentation = GamePresentation()
    assert actual == expected