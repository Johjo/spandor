namespace Spandor.Web;

public interface IQueryBus
{
    public Task<TResponse> Dispatch<TResponse>(IQuery<TResponse> query);
}