
class ClientError(Exception):
    pass

class AuthenticationError(ClientError):
    pass

class NotFoundError(ClientError):
    pass

class ServerError(Exception):
    pass