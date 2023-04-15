from typing import List
from pydantic import BaseModel

from fastapi import FastAPI
from middleware import RequestHandlingMiddleware
from starlette.middleware.base import BaseHTTPMiddleware

from services.cinemas import ManageCinema, Cinema
from services.afisha import ManageAfisha, SessionAfisha

app = FastAPI()
exception_handler = RequestHandlingMiddleware()
app.add_middleware(BaseHTTPMiddleware, dispatch=exception_handler)


class CinemaResponse(BaseModel):
    cinemas: List[Cinema]


class AfishaResponse(BaseModel):
    afisha: List[SessionAfisha]


@app.get("/api/cinemas", response_model=CinemaResponse)
def read_cinemas() -> CinemaResponse:
    """
    Endpoint for retrieving cinema data from all cinemas.
    """
    cinemas = ManageCinema().get_cinemas
    return CinemaResponse(cinemas=cinemas)


@app.get("/api/cinema/{cinema_id}", response_model=AfishaResponse)
def read_item(cinema_id: int) -> AfishaResponse:
    """
    Endpoint for retrieving Afisha data for a specific cinema.

    Args:
        cinema_id: An integer representing the cinema ID.
    """
    afisha = ManageAfisha(cinema_id).get_cinemas
    return AfishaResponse(afisha=afisha)
