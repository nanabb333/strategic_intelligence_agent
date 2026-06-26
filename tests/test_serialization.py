from dataclasses import dataclass

from serialization import serializable


@dataclass
class SampleItem:
    name: str
    count: int


def test_serializable_converts_nested_dataclasses() -> None:
    payload = {
        "items": [SampleItem("alpha", 2)],
        "plain": "value",
    }

    assert serializable(payload) == {
        "items": [{"name": "alpha", "count": 2}],
        "plain": "value",
    }
