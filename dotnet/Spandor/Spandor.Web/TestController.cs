using Microsoft.AspNetCore.Mvc;

namespace Spandor.Web;

public class TestController : ControllerBase
{

    [Route("test")]
    [HttpGet]
    public string Test()
    {
        throw new NotImplementedException();
    }
    
}