from fastapi import Request
from fastapi.responses import JSONResponse


class RequestHandlingMiddleware:
    """
    Middleware for handling requests and returning appropriate responses.
    """

    async def __call__(self, request: Request, call_next: callable) -> JSONResponse:
        """
        Handle incoming requests and return appropriate responses.
        """
        try:
            response = await call_next(request)
        except Exception as error:
            return JSONResponse(status_code=500, content={'detail': str(error)})

        return response
