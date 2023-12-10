public class Startup
{
    public void ConfigureServices(IServiceCollection services)
    {
        services.AddControllers();
    }
    public void Configure(IApplicationBuilder app, IConfiguration config)
    {
        app
            .UseRouting()
            // .UseSwagger(s => s.RouteTemplate = "internal/swagger/{documentName}/swagger.json")
            .UseEndpoints(ep => ep.MapControllers());
    }
}