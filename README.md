# Cinema Management

This project allows you to retrieve cinema session schedules. It uses the cinema API and web scraping to obtain data on session schedules and cinema information.


Installation:

Clone the repository: git clone https://github.com/ismailov0/Cinema-Management.git
Navigate to the project folder: cd cinema-management
```sh
$ pip install -r requirements.txt
$ uvicorn main:app --reload
```

Open your browser to http://localhost:8000/docs to view the app or to view API.

# Endpoints:
Endpoint for retrieving cinema data from all cinemas:
```sh
http://localhost:8000/api/cinemas
```

Endpoint for retrieving cinema session by id:
```sh
http://localhost:8000/api/cinema/{id}
```
