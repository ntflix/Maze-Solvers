from typing import Generic, Protocol, TypeVar


T = TypeVar("T")


class FileHandler(Generic[T], Protocol):
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

    def __close(self) -> None:
        raise NotImplementedError(
            "Cannot call __close() on protocol class",
        )
