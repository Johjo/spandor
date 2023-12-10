using Microsoft.AspNetCore.Hosting;
using Microsoft.AspNetCore.TestHost;

namespace Spandor.Web.Tests;

public class UnitTest1
{
    private readonly HttpClient _client;

    public UnitTest1()
    {
        var server = new TestServer(new WebHostBuilder());
        _client = server.CreateClient();
    }

    [Fact]
    public async Task ReturnHelloWorld()
    {
        var response = await _client.GetAsync("/");
        response.EnsureSuccessStatusCode();
        var responseString = await response.Content.ReadAsStringAsync();
        // Assert
        Assert.Equal("Hello World!", responseString);
    }
}