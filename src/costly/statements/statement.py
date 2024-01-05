from abc import abstractmethod
from datetime import date
from pathlib import Path
from typing import Protocol, Union
from typing import runtime_checkable
import pandas as pd


@runtime_checkable
class IAccountStatement(Protocol):
    account: str
    name: str
    start_date: date
    end_date: date
    data: pd.DataFrame

    @classmethod
    @abstractmethod
    def from_csv(cls, path: Union[str, Path]):
        """
        This constructor initializes an object of class `IAccountStatement` 
        from a comma-separated values (csv) file.

        Args:
            path (Union[str, Path]): The file path to the csv file.
        """
        ...

    @staticmethod
    @abstractmethod
    def _parse_account(df: pd.DataFrame) -> str:
        """
        This method parses the account number of the account holder.

        Args:
            df (pd.DataFrame): A data frame holding the raw data.

        Returns:
            str: The account number of the account holder.
        """
        ...

    @staticmethod
    @abstractmethod
    def _parse_name(df: pd.DataFrame) -> str:
        """
        This method parses the name of the account holder.

        Args:
            df (pd.DataFrame): A data frame holding the raw data.

        Returns:
            str: The name of the account holder.
        """
        ...

    @staticmethod
    @abstractmethod
    def _parse_start_date(df: pd.DataFrame) -> date:
        """
        This method parses the start date (earliest date) of the account 
        statement.

        Args:
            df (pd.DataFrame): A data frame holding the raw data.

        Returns:
            date: The start date on the account statement.
        """
        ...

    @staticmethod
    @abstractmethod
    def _parse_end_date(df: pd.DataFrame) -> date:
        """
        This method parses the end date (most recent date) of the account 
        statement.

        Args:
            df (pd.DataFrame): A data frame holding the raw data.

        Returns:
            date: The end date on the account statement.
        """
        ...