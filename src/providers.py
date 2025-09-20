from random import randint

from dishka import Provider, Scope, provide, provide_all

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
