using System.Reflection;
using MediatR;

namespace Spandor.Web;

public class Startup
{
    public void ConfigureServices(IServiceCollection services)
    {
        services.AddControllers();
        // services.AddScoped<IQueryBus, QueryBus>();
        // services.AddMediatR(Assembly.GetExecutingAssembly());
    }
    
    public void Configure(IApplicationBuilder app, IConfiguration config)
    {
        app
            .UseRouting()
            // .UseSwagger(s => s.RouteTemplate = "internal/swagger/{documentName}/swagger.json")
            .UseEndpoints(ep => ep.MapControllers());
    }
}