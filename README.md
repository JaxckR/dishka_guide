### Краткое руководство для dishka

1. Создадим абстрактный протокол, его реализацию, а также класс, который будет выполнять некую бизнес-логику
```Python
# interfaces
from abc import abstractmethod
from typing import Protocol


class Foo(Protocol):

    @abstractmethod
    def calculate(self) -> int:
        ...
```

```Python
# implementation
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

```

2. Напишем следующий провайдер
```Python
# providers
from random import randint

from dishka import Provider, Scope, provide

from implementation import Service, Boo
from interfaces import Foo


class DishkaProvider(Provider):
    scope = Scope.APP

    service = provide(
        Service,
        scope=Scope.REQUEST  # Перезаписывает область видимости провайдера
    )

    foo_impl = provide(
        Boo,
        provides=Foo,
    )

    @provide(scope=Scope.REQUEST)
    def get_some_string(self) -> str:
        return chr(randint(10_000, 100_000))

```
Scope управляет временем жизни зависимости<br>
Самые используемые - APP и REQUEST. При Scope.APP зависимость создается лишь единожды. При Scope.REQUEST на каждый вызов. Для большей информации - https://dishka.readthedocs.io/en/stable/advanced/scopes.html#scopes
<br>

С помощью provide мы можем доставать из контейнера необходимые нам зависимости.<br>
Сначала указываем что мы будем получать и если нужно заменить некий интерфейс, то указываем его аргументом provides<br>
Provide также можно использовать как декоратор. Возвращаемые тип будет использоваться как аргумент provides<br>
Если нам необходимо запровайдить несколько зависимостей не используя замену, то можно воспользоваться provide_all
```Python
from dishka import Provider, Scope, provide_all

class SomeProvider(Provider):
    scope = Scope.APP

    services = provide_all(
        Service1,
        Service2,
        ...
    )
```

3. Сценарий использования
```Python
from dishka import make_container

from implementation import Service
from interfaces import Foo
from providers import DishkaProvider


def main() -> None:
    container = make_container(DishkaProvider())

    with container() as cont:
        service = cont.get(Service)
        foo_impl = cont.get(Foo)

        print(service())
        print(service.string)
        print(foo_impl.calculate())


if __name__ == '__main__':
    main()
```