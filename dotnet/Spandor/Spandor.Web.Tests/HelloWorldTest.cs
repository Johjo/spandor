using System.Net;
using FluentAssertions;
using Microsoft.AspNetCore.Mvc.Testing;

namespace Spandor.Web.Tests;

public class WeatherForecastControllerTests
{
    [Fact]
    public async Task GET_retrieves_weather_forecast()
    {
        await using var application = new WebApplicationFactory<Startup>();
        using var client = application.CreateClient();
 
        var response = await client.GetAsync("/test");
        response.StatusCode.Should().Be(HttpStatusCode.OK);
    }
}