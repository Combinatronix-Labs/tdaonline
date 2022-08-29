from abc import ABC, abstractmethod


class Result(ABC):
    @abstractmethod
    def isError(self) -> bool:
        pass

    @abstractmethod
    def toJSON(self) -> str:
        pass

    def isSuccessful(self):
        return not self.isError()
