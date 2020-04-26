from typing import Dict, Any
import logging
from gmail import GMail

from .abstract_email_app import AbstractEmailApp


class GmailEmailApp(AbstractEmailApp):
    __slots__ = '__handler__'

    __handler__: GMail
    logger = logging.getLogger('GmailEmailApp')

    def __init__(self, email_address: str, api_key: str) -> None:
        """
        The basic constructor. Creates a new instance of EmailApp using the specified credentials

        :param api_key:
        """

        self.__handler__ = self.get_handler(email_address=email_address, api_key=api_key)
        super().__init__()

    @staticmethod
    def get_handler(email_address: str, api_key: str) -> GMail:
        """
        Returns an EmailApp handler.

        :param api_key:
        :return:
        """

        gmail_handler = GMail(username=email_address, password=api_key)
        gmail_handler.connect()
        return gmail_handler