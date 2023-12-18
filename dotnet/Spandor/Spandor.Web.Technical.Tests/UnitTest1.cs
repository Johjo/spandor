using Microsoft.AspNetCore.Hosting;
using Microsoft.AspNetCore.TestHost;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;

namespace Spandor.Web.Technical.Tests;

public class UnitTest1
{
    private readonly HttpClient _client;

    public UnitTest1()
    {
        var host = Host
            .CreateDefaultBuilder()
            .ConfigureWebHostDefaults(
                webBuilder => webBuilder
                    .UseStartup<Startup>()
                    .UseTestServer(o => o.BaseAddress = new Uri("https://localhost/")))
            .Build();
        host.StartAsync();
        _client = host.GetTestClient();

    }
    [Fact]
    public void Test1()
    {
    }
}