from abc import abstractmethod
from typing import Protocol


class Foo(Protocol):

    @abstractmethod
    def calculate(self) -> int:
        ...
