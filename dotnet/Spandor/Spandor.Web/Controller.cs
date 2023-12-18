using Microsoft.AspNetCore.Mvc;

namespace Spandor.Web;

public class Controller : ControllerBase
{
    private readonly IQueryBus _bus;

    public Controller(IQueryBus bus)
    {
        _bus = bus;
    }
    
    [Route("game")]
    public Task<GamePresentation> GetGame()
    {
        return _bus.Dispatch(new GetGameQuery());
    }
    
    
    
}