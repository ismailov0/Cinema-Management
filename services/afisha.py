from datetime import datetime
import requests
from typing import List, TypedDict, TypeAlias, Optional, Union

from services.exceptions import ParsingError

hallName: TypeAlias = str


class Session(TypedDict):
    """TypedDict for a cinema session."""

    session_date_tz: Optional[str]
    movie_name: str


class SessionAfisha(TypedDict):
    """TypedDict for a cinema session schedule."""

    hall_name: str
    sessions: str | List[Session]


class ManageAfisha:
    """Class for managing cinema session schedules."""

    def __init__(self, cinema_id: int) -> None:
        """Initialize the ManageAfisha class with a cinema ID."""

        self.current_date = datetime.now().strftime('%Y-%m-%d')
        self.url: str = f'https://api.kino.kz/sessions/v1/cinema/sessions?cinema_id={cinema_id}&date={self.current_date}&filter_by=halls'

    @property
    def get_cinemas(self) -> List[SessionAfisha]:
        """Get a list of cinema session schedules."""

        response = self._get_response()
        return self._parse_json(response)

    def _get_response(self) -> str:
        """Send a request to the cinema session API and return the response as a string."""

        try:
            response = requests.get(self.url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException:
            raise ParsingError('Error occurred while request data')

    def _parse_json(self, sessions: str) -> List[SessionAfisha]:
        """
        Parse a JSON string containing cinema session data
                and return a list of SessionAfisha objects.
        """
        sessions = sessions['result']['sessions']

        if not sessions:
            raise ParsingError('The cinema not found')

        data = []
        for session in sessions:
            hall_information = SessionAfisha(
                {'hall_name': session['hall']['name'],
                 'sessions': self._parse_sessions(session['items'])
                 }
            )
            data.append(hall_information)
        return data

    def _parse_sessions(self, sessions: List[dict]) -> List[Session]:
        """Parse a list of cinema session dictionaries and return a list of Session objects."""

        sessions_list = []
        for session in sessions:
            sessions_list.append(Session(
                {
                    'session_date_tz': session['session']['session_date_tz'],
                    'movie_name': session['movie']['name_rus']
                }
            )
            )
        return sessions_list
