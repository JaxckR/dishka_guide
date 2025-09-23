# Краткое руководство для dishka

Dishka является DI библиотекой, которая предоставляет мощный IoC контейнер.

## Что такое IoC и DI?

**Inversion of control (IoC)** - Принцип, суть которого отдать управление жизненным циклом своих зависимостей и себя
самого внешнему контейнеру или фреймворку.<br>
**Dependency injection (DI)** - практика внедрения зависимостей из вне, является частным случаем реализации IoC.
Внедрять зависимости можно через конструктор, сеттеры и др.<br>

## Сценарий использования

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

Провайдер является ключевым компонентом ioc контейнера в dishka. Один контейнер может принимать множество
провайдеров. <br>
Чтобы воспользоваться механизмом DI, мы должны создать атрибут и присвоить ему результат функции provide.<br>
Функция provide принимает в себя один обязательный аргумент - функцию/класс или любой другой callable объект.
Также он принимает в себя параметр provides, он позволяет заменять аргумент provides на то, что мы указали первым
аргументом.<br>

Существует функция provide_all, которая выполняет ту же самую функцию, что и provide, но не принимает в себя параметр
provides<br>

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

Scope управляет временем жизни зависимости<br>
Самые используемые - APP и REQUEST. 
При Scope.APP зависимость создается лишь единожды. При Scope.REQUEST на каждый вызов. 
Для большей информации - https://dishka.readthedocs.io/en/stable/advanced/scopes.html#scopes
<br>

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