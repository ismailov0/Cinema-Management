from fastapi import FastAPI
from middleware import RequestHandlingMiddleware
from pydantic import BaseModel
from services.afisha import ManageAfisha, SessionAfisha
from services.cinemas import Cinema, ManageCinema
from starlette.middleware.base import BaseHTTPMiddleware
from typing import List


# Create the FastAPI app
app = FastAPI()

# Define the middleware for handling exceptions
exception_handler = RequestHandlingMiddleware()

# Add the middleware to the app
app.add_middleware(BaseHTTPMiddleware, dispatch=exception_handler)


class CinemaResponse(BaseModel):
    """
    The response model for getting a list of cinemas.
    """
    cinemas: List[Cinema]


class AfishaResponse(BaseModel):
    """
    The response model for getting a list of afisha sessions.
    """
    afisha: List[SessionAfisha]


@app.get("/api/cinemas", response_model=CinemaResponse)
def read_cinemas() -> CinemaResponse:
    """
    Endpoint for retrieving all cinemas.
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
