from costly.statements.reader import IStatementReader, KBCStatementReader
import pytest


def test_subtyping():
    kbc_reader = KBCStatementReader()
    assert isinstance(kbc_reader, KBCStatementReader)
    assert isinstance(kbc_reader, IStatementReader)