using MediatR;

namespace Spandor.Web;

public class QueryBus : IQueryBus
{
    private readonly IMediator _mediator;

    public QueryBus(IMediator mediator)
    {
        _mediator = mediator;
    }
    
    
    public async Task<TResponse> Dispatch<TResponse>(IQuery<TResponse> query)
    {
        return await _mediator.Send(query);
    }
}