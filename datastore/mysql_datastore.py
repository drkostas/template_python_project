from typing import List, Tuple
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from datetime import datetime

from .abstract_datastore import AbstractDatastore


class MySqlDataStore(AbstractDatastore):
    def __init__(self, username: str, password: str, hostname: str, dbname: str) -> None:
        """
        Tha basic constructor. Creates a new instance of a MySQL Datastore using the specified credentials

        :param username:
        :param password:
        :param hostname:
        :param dbname:
        """

        super().__init__(username=username, password=password,
                         hostname=hostname, dbname=dbname)

    @staticmethod
    def get_connection(username: str, password: str, hostname: str, dbname: str) -> Tuple:
        """
        Creates and returns a connection and a cursor/session to the MySQL DB

        :param username:
        :param password:
        :param hostname:
        :param dbname:
        :return:
        """

        engine = create_engine("mysql://{}:{}@{}/{}".format(username, password, hostname, dbname))
        session_obj = sessionmaker(bind=engine)
        session = scoped_session(session_obj)
        return engine, session

    def create_table(self, table: str, schema: str) -> None:
        """
        Creates a table using the specified schema

        :param table:
        :param schema:
        :return:
        """

        query = "CREATE TABLE {table} ({schema})".format(table=table, schema=schema)
        self.__cursor__.execute(query)
        self.__cursor__.commit()

    def drop_table(self, table: str) -> None:
        """
        Drops the specified table if it exists

        :param table:
        :return:
        """

        query = "DROP TABLE IF EXISTS {table}".format(table=table)
        self.__cursor__.execute(query)
        self.__cursor__.commit()

    def truncate_table(self, table: str) -> None:
        """
        Truncates the specified table

        :param table:
        :return:
        """

        query = "TRUNCATE TABLE {table}".format(table=table)
        self.__cursor__.execute(query)
        self.__cursor__.commit()

    def insert_into_table(self, table: str, data: dict) -> None:
        """
        Inserts into the specified table a row based on a column_name: value dictionary

        :param table:
        :param data:
        :return:
        """

        data_str = ", ".join(
            list(map(lambda key, val: "{key}='{val}'".format(key=str(key), val=str(val)), data.keys(), data.values())))

        query = "INSERT INTO {table} SET {data}".format(table=table, data=data_str)
        self.__cursor__.execute(query)
        self.__cursor__.commit()

    def update_table(self, table: str, set_data: dict, where: str) -> None:
        """
        Updates the specified table using a column_name: value dictionary and a where statement

        :param table:
        :param set_data:
        :param where:
        :return:
        """

        set_data_str = ", ".join(
            list(map(lambda key, val: "{key}='{val}'".format(key=str(key), val=str(val)), set_data.keys(),
                     set_data.values())))

        query = "UPDATE {table} SET {data} WHERE {where}".format(table=table, data=set_data_str, where=where)
        self.__cursor__.execute(query)

    def select_from_table(self, table: str, columns: str = '*', where: str = 'TRUE', order_by: str = 'NULL',
                          asc_or_desc: str = 'ASC', limit: int = 1000) -> List:
        """
        Selects from a specified table based on the given columns, where, ordering and limit

        :param table:
        :param columns:
        :param where:
        :param order_by:
        :param asc_or_desc:
        :param limit:
        :return results:
        """

        query = "SELECT * FROM  {table} WHERE {where} ORDER BY {order_by} {asc_or_desc} LIMIT {limit}".format(
            table=table, where=where, order_by=order_by, asc_or_desc=asc_or_desc, limit=limit)
        results = self.__cursor__.execute(query).fetchall()
        return results

    def delete_from_table(self, table: str, where: str) -> None:
        """
        Deletes data from the specified table based on a where statement

        :param table:
        :param where:
        :return:
        """

        query = "DELETE FROM {table} WHERE {where}".format(table=table, where=where)
        self.__cursor__.execute(query)

    def __exit__(self) -> None:
        """
        Flushes and closes the connection

        :return:
        """

        self.__cursor__.flush()
        self.__cursor__.commit()
        self.__cursor__.close()
