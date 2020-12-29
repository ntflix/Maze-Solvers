from typing import Any, Protocol


class Serializable(Protocol):
    def serialize(self) -> Any:
        """Return a serializable representation of the object.

        Returns:
            Any: The serialized representation of the object.
        """
        raise NotImplementedError()