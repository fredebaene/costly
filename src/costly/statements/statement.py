from abc import abstractmethod
from costly.statements.reader import IStatementReader
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
        data = statement_reader.from_csv(path)
        return cls(
            account=data["account"],
            name=data["name"],
            start_date=data["start_date"],
            end_date=data["end_date"],
            data=data["data"]
        )