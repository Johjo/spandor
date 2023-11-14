using Microsoft.AspNetCore.TestHost;
using Microsoft.Extensions.Hosting;

namespace Spandor.Web.tests;

public class UnitTest1
{
    [Fact]
    public void ShouldRetrieveNoGameStarted()
    {
        IHost host = new HostBuilder().Build();
        HttpClient httpClient = host.GetTestClient();
    }
}