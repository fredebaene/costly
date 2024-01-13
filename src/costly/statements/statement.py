from abc import abstractmethod
from costly.statements.reader import IStatementReader, KBCStatementReader
from datetime import date
from pathlib import Path
from typing import Optional, Union
import pandas as pd


class AccountStatement:
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
    def from_csv(
            cls,
            path: Union[str, Path],
            statement_reader: IStatementReader):
        data = statement_reader.read_csv(path)
        return cls(
            account=data["account"],
            name=data["name"],
            start_date=data["start_date"],
            end_date=data["end_date"],
            data=data["data"]
        )
    
    def sum_transactions(self) -> float:
        """
        This method sums the transactions in the given statement, both 
        incoming and outgoing transactions.

        Returns:
            float: The summed transactions.
        """
        return self.data["amount"].sum()
    
    def sum_incoming(self) -> float:
        """
        This method sums the incoming transactions in the statement.

        Returns:
            float: The summed incoming transactions.
        """
        return self.data["credit"].sum()
    
    def sum_outgoing(self) -> float:
        """
        This method sums the outgoing transactions in the statement.

        Returns:
            float: The summed outgoing transactions.
        """
        return self.data["debit"].sum()