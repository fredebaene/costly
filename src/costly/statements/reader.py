from abc import abstractmethod
from datetime import date
from pathlib import Path
from typing import Protocol, Tuple, Union
from typing import runtime_checkable
import pandas as pd


@runtime_checkable
class IStatementReader(Protocol):
    data: dict

    def read_csv(self, path: Union[str, Path]) -> dict:
        """
        This method reads and parses the data from a comma-separated values 
        file (csv file) that contains the raw data.

        Args:
            path (Union[str, Path]): The path to the csv file.

        Returns:
            dict: A dictionary containing the required items.
        """
        ...
    
    def _clean_raw_data(self, df: pd.DataFrame) -> None:
        """
        This method cleans the raw data. This comprises renaming the fields 
        and dropping redundant fields. The clean data is added to the instance 
        attribute `data`, which is a dict, with the key `data`.

        Args:
            df (pd.DataFrame): A data frame holding the raw data.
        """
        ...
    
    def _parse_account(self, df: pd.DataFrame) -> None:
        """
        This method parses the account number of the account holder. The 
        account number is added to the instance attribute `data`, which is a 
        dict, with the key `account`.

        Args:
            df (pd.DataFrame): A data frame holding the raw data.
        """
        ...
    
    def _parse_name(self, df: pd.DataFrame) -> None:
        """
        This method parses the name of the account holder. The name is added 
        to the instance attribute `data`, which is a dict, with the key 
        `name`.

        Args:
            df (pd.DataFrame): A data frame holding the raw data.
        """
        ...
    
    def _parse_start_date(self, df: pd.DataFrame) -> None:
        """
        This method parses the start date (earliest date) of the account 
        statement. The start data is added to the instance attribute `data`, 
        which is a dict, with the key `start_date`.

        Args:
            df (pd.DataFrame): A data frame holding the raw data.
        """
        ...
    
    def _parse_end_date(self, df: pd.DataFrame) -> None:
        """
        This method parses the end date (most recent date) of the account 
        statement. The end data is added to the instance attribute `data`, 
        which is a dict, with the key `end_date`.

        Args:
            df (pd.DataFrame): A data frame holding the raw data.
        """
        ...


class KBCStatementReader:
    def __init__(self) -> None:
        self.data = {}
    
    def read_csv(self, path: Union[str, Path]) -> dict:
        """
        This method reads and parses the data from a comma-separated values 
        file (csv file) that contains the raw data.

        Args:
            path (Union[str, Path]): The path to the csv file.

        Returns:
            dict: A dictionary containing the required items.
        """
        path = Path(path) if isinstance(path, str) else path
        df = pd.read_csv(path, sep=";")
        self._parse_account(df)
        self._parse_name(df)
        self._parse_start_date(df)
        self._parse_end_date(df)
        self._clean_raw_data(df)
        return self.data
    
    def _clean_raw_data(self, df: pd.DataFrame) -> None:
        """
        This method cleans the raw data. This comprises renaming the fields 
        and dropping redundant fields. The clean data is added to the instance 
        attribute `data`, which is a dict, with the key `data`.

        Args:
            df (pd.DataFrame): A data frame holding the raw data.
        """
        col_names = {
            "Munt": "currency",
            "Afschriftnummer": "copy_number",
            "Datum": "date",
            "Omschrijving": "Description",
            "Valuta": "value_date",
            "Bedrag": "amouunt",
            "Saldo": "balance",
            "rekeningnummer tegenpartij": "account_opposite",
            "BIC tegenpartij": "bic_opposite",
            "Naam tegenpartij": "name_opposite",
            "Adres tegenpartij": "address_opposite",
            "gestructureerde mededeling": "structured_reference",
            "Vrije mededeling": "unstructured_reference",
        }
        self.data["data"] = (
            df
            .rename(columns=col_names)
            [[*list(col_names.values())]]
        )
    
    def _parse_account(self, df: pd.DataFrame) -> None:
        """
        This method parses the account number of the account holder. The 
        account number is added to the instance attribute `data`, which is a 
        dict, with the key `account`.

        Args:
            df (pd.DataFrame): A data frame holding the raw data.
        """
        self.data["account"] = df["Rekeningnummer"].drop_duplicates().iloc[0]
    
    def _parse_name(self, df: pd.DataFrame) -> None:
        """
        This method parses the name of the account holder. The name is added 
        to the instance attribute `data`, which is a dict, with the key 
        `name`.

        Args:
            df (pd.DataFrame): A data frame holding the raw data.
        """
        self.data["name"] = df["Naam"].drop_duplicates().iloc[0]
    
    def _parse_start_date(self, df: pd.DataFrame) -> None:
        """
        This method parses the start date (earliest date) of the account 
        statement. The start data is added to the instance attribute `data`, 
        which is a dict, with the key `start_date`.

        Args:
            df (pd.DataFrame): A data frame holding the raw data.
        """
        self.data["start_date"] = df["Datum"].min()
    
    def _parse_end_date(self, df: pd.DataFrame) -> None:
        """
        This method parses the end date (most recent date) of the account 
        statement. The end data is added to the instance attribute `data`, 
        which is a dict, with the key `end_date`.

        Args:
            df (pd.DataFrame): A data frame holding the raw data.
        """
        self.data["end_date"] = df["Datum"].max()
