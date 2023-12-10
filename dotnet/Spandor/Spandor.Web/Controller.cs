using Microsoft.AspNetCore.Mvc;

namespace Spandor.Web;

public class Controller : ControllerBase
{
    [Route("game")]
    public GamePresentation GetGame()
    {
        return new GamePresentation();
    }
    
    
    
}