from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from common.dynamodb import ProductRepository


def test_repository_uses_table_name(monkeypatch):
    class FakeTable:
        def __init__(self): self.calls = []
        def get_item(self, Key): return {}
    class FakeResource:
        def __init__(self, *args, **kwargs): self.Table = lambda name: FakeTable()
    monkeypatch.setattr("common.dynamodb.boto3.resource", FakeResource)
    repo = ProductRepository(table_name="test-table")
    assert repo.table_name == "test-table"
