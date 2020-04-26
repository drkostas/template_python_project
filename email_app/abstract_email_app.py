from abc import ABC, abstractmethod


class AbstractEmailApp(ABC):
    __slots__ = ('__handler__',)

    @abstractmethod
    def __init__(self, *args, **kwargs) -> None:
        """
        Tha basic constructor. Creates a new instance of EmailApp using the specified credentials

        """

        pass

    @staticmethod
    @abstractmethod
    def get_handler(*args, **kwargs):
        """
        Returns an EmailApp handler.

        :param args:
        :param kwargs:
        :return:
        """

        pass