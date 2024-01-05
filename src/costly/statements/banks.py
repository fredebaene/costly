from datetime import date
from pathlib import Path
from costly.statements.statement import IAccountStatement
from typing import Union
import pandas as pd


class KBCAccountStatement:
    def __init__(
            self,
            account: str,
            name: str,
            start_date: date,
            end_date: date,
            data: pd.DataFrame) -> None:
        self.account = account
        self.name = name
        self.start_date = start_date
        self.end_date = end_date
        self.data = data

    @classmethod
    def from_csv(cls, path: Union[str, Path]):
        """
        This constructor initializes an object of class `IAccountStatement` 
        from a comma-separated values (csv) file.

        Args:
            path (Union[str, Path]): The file path to the csv file.
        """
        path = Path(path) if isinstance(path, str) else path
        df = pd.read_csv(path, sep=";")
        return cls(
            account=cls._parse_account(df),
            name=cls._parse_name(df),
            start_date=cls._parse_start_date(df),
            end_date=cls._parse_end_date(df),
            data=cls._clean_raw_data(df),
        )
    
    @staticmethod
    def _clean_raw_data(df: pd.DataFrame) -> pd.DataFrame:
        """
        This method cleans the raw data. This comprises renaming the fields 
        and dropping redundant fields.

        Args:
            df (pd.DataFrame): A data frame holding the raw data.

        Returns:
            pd.DataFrame: A data frame with clean data.
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
        return df.rename(columns=col_names)[[*list(col_names.values())]]

    @staticmethod
    def _parse_account(df: pd.DataFrame) -> str:
        """
        This method parses the account number of the account holder.

        Args:
            df (pd.DataFrame): A data frame holding the raw data.

        Returns:
            str: The account number of the account holder.
        """
        return df["Rekeningnummer"].drop_duplicates().iloc[0]

    @staticmethod
    def _parse_name(df: pd.DataFrame) -> str:
        """
        This method parses the name of the account holder.

        Args:
            df (pd.DataFrame): A data frame holding the raw data.

        Returns:
            str: The name of the account holder.
        """
        return df["Naam"].drop_duplicates().iloc[0]

    @staticmethod
    def _parse_start_date(df: pd.DataFrame) -> date:
        """
        This method parses the start date (earliest date) of the account 
        statement.

        Args:
            df (pd.DataFrame): A data frame holding the raw data.

        Returns:
            date: The start date on the account statement.
        """
        return df["Datum"].min()

    @staticmethod
    def _parse_end_date(df: pd.DataFrame) -> date:
        """
        This method parses the end date (most recent date) of the account 
        statement.

        Args:
            df (pd.DataFrame): A data frame holding the raw data.

        Returns:
            date: The end date on the account statement.
        """
        return df["Datum"].max()
