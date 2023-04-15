from fastapi import HTTPException

def handle_exceptions(func):
    def wrapper(*args):
        try:
            return func(*args)
        except ParsingError as error:
            raise HTTPException(status_code=500, detail=str(error))
        except Exception as error:
            raise HTTPException(status_code=500, detail=str(error))
    return wrapper

class ParsingError(Exception):
    pass