using System.Text.Json;
using AutoFixture.Xunit2;
using FluentAssertions;
using Microsoft.AspNetCore.Hosting;
using Microsoft.AspNetCore.TestHost;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;

namespace Spandor.Web.Tests;

public class GetGameQueryTests
{
    private readonly HttpClient _client;
    private readonly StubbedQueryBus _queryBus;

    public GetGameQueryTests()
    {
        _queryBus = new StubbedQueryBus();
        var host = Host
            .CreateDefaultBuilder()
            .ConfigureWebHostDefaults(
                webBuilder => webBuilder
                    .UseStartup<Startup>()
                    .UseTestServer(o => o.BaseAddress = new Uri("https://localhost/")))
            .ConfigureServices(
                services => services.AddSingleton<IQueryBus>(_queryBus))
            .Build();
        host.StartAsync();
        _client = host.GetTestClient();
    }
    
    [Theory, AutoData]
    public async Task Should_get_game(GetGameQuery query, GamePresentation expected)
    {
        _queryBus.Feed(query, expected);

        var response = await _client.GetAsync("/game");
        response.EnsureSuccessStatusCode();
        
        var responseContent = await response.Content.ReadAsStringAsync();
        responseContent.Should().Be(Serialize(expected));
    }

    private static string Serialize(GamePresentation expected)
    {
        var expectedJson = JsonSerializer.Serialize(expected,
            new JsonSerializerOptions { PropertyNamingPolicy = JsonNamingPolicy.CamelCase });
        return expectedJson;
    }
}

public class StubbedQueryBus : IQueryBus
{
    private readonly Dictionary<string, GamePresentation> _presentations = new();
    
    public void Feed(GetGameQuery query, GamePresentation expected)
    {
        _presentations[ToKey(query)] = expected;
    }


    public GamePresentation Dispatch(GetGameQuery query)
    {
        return _presentations[ToKey(query)];
    }

    private static string ToKey(GetGameQuery query)
    {
        return JsonSerializer.Serialize(query);
    }
}