from ..result import Result
import json


class ErrorResult(Result):
    """"Use ErrorResult for a general error result"""

    def isError(self) -> bool:
        return True

    def toJSON(self) -> str:
        return json.dumps({
            'message': self.message
        })

    def __init__(self, message: str) -> None:
        super().__init__()
        self.message = message

    def __repr__(self) -> str:
        return self.message


class FormattingErrorResult(ErrorResult):
    """Use FormattingErrorResult when there is an input formatting error"""

    def __init__(self) -> None:
        super().__init__("File format error.")


class InputSizeErrorResult(ErrorResult):
    """Use InputSizeErrorResult when the input recieved is too large"""

    def __init__(self, maxSize: int, inputLength: int) -> None:
        super().__init__(
            "Data too large! Please submit a data set with " + str(maxSize) +
            " points or fewer (your file contains " +
            str(inputLength) + " points)."
        )
