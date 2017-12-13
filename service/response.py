from enum import Enum

class ErrorCodeEnum(Enum):
    Success = 1
    ConnectionError = 2 # is this a reserved word?
    ParsingError = 3

class Response:
    """This class defines a simple response type for mpd_provider_module instructions"""
    errorCode = ErrorCodeEnum.Success
    suggestion = ""

    def __init__(self, success=ErrorCodeEnum.Success, suggestion=None):
        self.success = success
        self.suggestion = suggestion
