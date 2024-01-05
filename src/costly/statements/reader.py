from abc import abstractmethod
from datetime import date
from pathlib import Path
from typing import Protocol, TypeVar, Union
from typing import runtime_checkable


@runtime_checkable
class IAccountStatement(Protocol):
    account: str
    name: str
    start_date: date
    end_date: date

    @classmethod
    @abstractmethod
    def from_csv(cls, path: Union[str, Path]):
        ...

    @staticmethod
    @abstractmethod
    def _parse_account() -> str:
        ...

    @staticmethod
    @abstractmethod
    def _parse_name() -> str:
        ...

    @staticmethod
    @abstractmethod
    def _parse_start_date() -> date:
        ...

    @staticmethod
    @abstractmethod
    def _parse_end_date() -> date:
        ...