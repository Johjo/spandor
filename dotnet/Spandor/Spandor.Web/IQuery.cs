using MediatR;

namespace Spandor.Web;

public interface IQuery<out TResponse>: IRequest<TResponse>
{
}