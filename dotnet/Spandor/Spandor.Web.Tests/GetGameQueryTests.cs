using System.Text.Json;
using AutoFixture.Xunit2;
using FluentAssertions;
using Microsoft.AspNetCore.Hosting;
using Microsoft.AspNetCore.TestHost;

namespace Spandor.Web.Tests;

public class GetGameQueryTests
{
    private readonly HttpClient _client;

    public GetGameQueryTests()
    {
        var server = new TestServer(new WebHostBuilder().UseStartup<Startup>());
        _client = server.CreateClient();
    }
    
    [Theory, AutoData]
    public async Task Should_get_game(GetGameQuery query, GamePresentation expected)
    {
        var bus = new StubbedQueryBus();
        bus.Feed(query, expected);

        var response = await _client.GetAsync("/game");
        response.EnsureSuccessStatusCode();
        var responseContent = await response.Content.ReadAsStringAsync();
        var expectedJson = JsonSerializer.Serialize(expected);
        responseContent.Should().Be(expectedJson);
    }

}

public class StubbedQueryBus
{
    private Dictionary<GetGameQuery, GamePresentation> presentations = new();

    public void Feed(GetGameQuery query, GamePresentation expected)
    {
        this.presentations[query] = expected;
    }
}

public record GetGameQuery
{
}