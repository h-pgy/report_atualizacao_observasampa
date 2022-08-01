from requests.exceptions import HTTPError

class FichaNotFound(HTTPError):
    pass

class FichaForaPadrao(ValueError):
    pass