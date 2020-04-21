from abc import ABC, abstractmethod
from typing import List, Tuple

class AbstractDatastore(ABC):
    __slots__ = ('__connection__', '__cursor__')

    @abstractmethod
    def __init__(self, username: str, password: str, hostname: str, dbname: str) -> None:
        """
        Tha basic constructor. Creates a new instance of a Datastore using the specified credentials

        :param username:
        :param password:
        :param hostname:
        :param dbname:
        """

        self.__connection__, self.__cursor__ = self.get_connection(username=username, password=password,
                                                                   hostname=hostname,
                                                                   dbname=dbname)
    @staticmethod
    @abstractmethod
    def get_connection(username: str, password: str, hostname: str, dbname: str) -> Tuple:
        pass

    @abstractmethod
    def __exit__(self):
        pass

    @abstractmethod
    def create_table(self, table: str, schema: str):
        pass

    @abstractmethod
    def drop_table(self, table: str) -> None:
        pass

    @abstractmethod
    def truncate_table(self, table: str) -> None:
        pass

    @abstractmethod
    def insert_into_table(self, table: str, data: dict) -> None:
        pass

    @abstractmethod
    def update_table(self, table: str, set_data: dict, where: str) -> None:
        pass

    @abstractmethod
    def select_from_table(self, table: str, columns: str = '*', where: str = 'TRUE', order_by: str = 'NULL',
                          asc_or_desc: str = 'ASC', limit: int = 1000) -> List:
        pass

    @abstractmethod
    def delete_from_table(self, table: str, where: str) -> None:
        pass
