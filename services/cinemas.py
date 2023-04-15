import re
import requests
import json
from bs4 import BeautifulSoup

from typing import List, TypedDict, TypeAlias
from services.exceptions import ParsingError

CinemaDescription: TypeAlias = str


class Cinema(TypedDict):
    id: int
    name: str
    address: str
    city_name: str
    info_up: CinemaDescription


class ManageCinema:
    """This class is used to parse data from all cinemas. """

    def __init__(self) -> None:
        """Initializes the ManageCinema class with the URL of the kino.kz."""

        self.url: str = 'https://kino.kz/cinemas'

    @property
    def get_cinemas(self) -> List[Cinema]:
        """Returns a list of cinemas parsed from the kino.kz website."""

        response = self._get_response()
        return self._parse_html(response)

    def _get_response(self) -> str:
        """Sends a request to the kino.kz website and returns the response as text. """

        try:
            response = requests.get(self.url)
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException:
            raise ParsingError('Error occurred while request data')

    def _parse_html(self, html: str) -> List[Cinema]:
        """Parses the HTML of the kino.kz website and returns a list of cinemas."""

        try:
            soup = BeautifulSoup(html, 'html.parser')
            script = soup.find('script', {'id': '__NEXT_DATA__'})
            cinemas = json.loads(script.string)[
                'props']['pageProps']['cinemas']

            for cinema in cinemas:
                cinema['info_up'] = re.compile(
                    '<.*?>').sub('', cinema['info_up'])

            return cinemas
        except (KeyError, TypeError):
            raise ParsingError('Error occurred while parsing HTML')
