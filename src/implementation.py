from random import randint

from interfaces import Foo


class Boo(Foo):

    def calculate(self) -> int:
        return randint(1, 100) * randint(1, 100)


class Service:

    def __init__(self, foo: Foo, string: str) -> None:
        self.foo = foo
        self.string = string

    def __call__(self) -> int:
        ...  # Имитация некой логики
        return self.foo.calculate()
