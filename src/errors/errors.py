class ApiError(Exception):
    code = 422
    description = "Default message"

class InvalidUsernameOrPassword(ApiError):
    code = 400
    description = "The username or password is invalid"

class Unauthorized(ApiError):
    code = 401
    description = "Unauthorized"

class BadRequestApi(ApiError):
    code = 401
    description = "Bad request"
    def __init__(self, description) -> None:
        self.description = description