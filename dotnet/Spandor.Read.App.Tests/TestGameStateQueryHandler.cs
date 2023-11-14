using FluentAssertions;
using FluentAssertions.Execution;
using NFluent;

namespace Spandor.Read.App.Tests;

public class TestGameStateQueryHandler
{
    [Fact]
    public async Task ShouldGetNoGameWhenGameNotStarted()
    {
        var query = new GameStateQuery();
        var sut = new GameStateQueryHandler();

        var actual = await sut.Handle(query);
        var expected = new NoGamePresentation();

        actual.Should().Be(expected);
    }
}

public record NoGamePresentation;

public class GameStateQueryHandler
{
    public async Task<NoGamePresentation> Handle(GameStateQuery query)
    {
        return new NoGamePresentation();
    }
}

public record GameStateQuery
{
}