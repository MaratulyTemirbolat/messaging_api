# Python
from typing import (
    Any,
    Optional,
)


def cast_to_int(value: Any) -> Optional[int]:
    try:
        return int(value)
    except ValueError:
        return None
