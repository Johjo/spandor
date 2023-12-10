namespace Spandor.Web;

public interface IQueryBus
{
    public GamePresentation Dispatch(GetGameQuery query);
}