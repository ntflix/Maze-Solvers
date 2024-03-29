from modules.file_handling.serializable import Serializable
from typing import Generic, Protocol, TypeVar

T = TypeVar("T", bound=Serializable)


class FileHandler(Protocol, Generic[T]):  # type: ignore  # issues conforming to both Generic and Protocol
    """A file handler protocol for any FileHandler objects to conform to. Abstract only."""

    def __init__(self, path: str) -> None:
        raise NotImplementedError(
            "Cannot call __init__() on protocol class",
        )

    def load(self) -> T:
        raise NotImplementedError(
            "Cannot call load() on protocol class",
        )

    def save(self, object: T) -> None:
        raise NotImplementedError(
            "Cannot call save() on protocol class",
        )
