"""Serialization helpers for run artifacts."""

from __future__ import annotations

from dataclasses import asdict, is_dataclass
from typing import Any


def serializable(value: Any) -> Any:
    """Convert dataclasses, lists, and dictionaries into JSON-friendly objects."""
    if is_dataclass(value):
        return asdict(value)
    if isinstance(value, list):
        return [serializable(item) for item in value]
    if isinstance(value, dict):
        return {key: serializable(item) for key, item in value.items()}
    return value
