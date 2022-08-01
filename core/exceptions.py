from requests.exceptions import HTTPError

class FichaNotFound(HTTPError):
    pass