from abc import abstractmethod
from datetime import date
from pathlib import Path
from typing import Protocol, Tuple, Union
from typing import runtime_checkable
import pandas as pd


@runtime_checkable
class IStatementReader(Protocol):
    def read_csv(self, path: Union[str, Path]) -> Tuple[dict, pd.DataFrame]:
        """
        This method reads and parses the data from a comma-separated values 
        file (csv file) that contains the raw data.

        Args:
            path (Union[str, Path]): The path to the csv file.

        Returns:
            Tuple[dict, pd.DataFrame]: A tuple; the first element is a 
                dictionary holding metadata, the second element is a data 
                frame with clean data.
        """
        ...
    
    def _clean_raw_data(df: pd.DataFrame) -> pd.DataFrame:
        """
        This method cleans the raw data. This comprises renaming the fields 
        and dropping redundant fields.

        Args:
            df (pd.DataFrame): A data frame holding the raw data.

        Returns:
            pd.DataFrame: A data frame with clean data.
        """
        ...
    
    def _parse_account(df: pd.DataFrame) -> str:
        """
        This method parses the account number of the account holder.

        Args:
            df (pd.DataFrame): A data frame holding the raw data.

        Returns:
            str: The account number of the account holder.
        """
        ...
    
    def _parse_name(df: pd.DataFrame) -> str:
        """
        This method parses the name of the account holder.

        Args:
            df (pd.DataFrame): A data frame holding the raw data.

        Returns:
            str: The name of the account holder.
        """
        ...
    
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


class KBCStatementReader:    
    def read_csv(self, path: Union[str, Path]) -> Tuple[dict, pd.DataFrame]:
        """
        This method reads and parses the data from a comma-separated values 
        file (csv file) that contains the raw data.

        Args:
            path (Union[str, Path]): The path to the csv file.

        Returns:
            Tuple[dict, pd.DataFrame]: A tuple; the first element is a 
                dictionary holding metadata, the second element is a data 
                frame with clean data.
        """
        path = Path(path) if isinstance(path, str) else path
        df = pd.read_csv(path, sep=";")
        metadata = {}
        metadata["account"] = self._parse_account(df)
        metadata["name"] = self._parse_name(df)
        metadata["start_date"] = self._parse_start_date(df)
        metadata["end_date"] = self._parse_end_date(df)
        data = self._clean_raw_data(df)
        return (metadata, data)
    
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
    
    def _parse_account(df: pd.DataFrame) -> str:
        """
        This method parses the account number of the account holder.

        Args:
            df (pd.DataFrame): A data frame holding the raw data.

        Returns:
            str: The account number of the account holder.
        """
        return df["Rekeningnummer"].drop_duplicates().iloc[0]
    
    def _parse_name(df: pd.DataFrame) -> str:
        """
        This method parses the name of the account holder.

        Args:
            df (pd.DataFrame): A data frame holding the raw data.

        Returns:
            str: The name of the account holder.
        """
        return df["Naam"].drop_duplicates().iloc[0]
    
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
