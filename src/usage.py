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

