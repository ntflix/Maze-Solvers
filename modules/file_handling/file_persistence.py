from modules.file_handling.serializable import Serializable
from typing import Generic, TypeVar
import logging
import shelve

T = TypeVar("T", bound=Serializable)  # T has to conform to Serializable


class FilePersistence(Generic[T]):
    __path: str

    def __init__(self, path: str):
        self.__path = path

    def load(self, key: str) -> T:
        # define `maze` variable here to be used in function scope
        loaded: T

        #  open the maze file within a context manager
        try:
            with shelve.open(self.__path) as shelf:
                # load from file
                loaded = shelf[key]
        except KeyError as error:
            # make a nice error message :)
            errorMessage = f"File at {self.__path} is corrupt or does not exist."
            # log the error
            logging.error((errorMessage, error))
            # aaand raise a not so nice error with the nice message for the happy user
            raise FileNotFoundError(errorMessage)

        if isinstance(loaded, T):  # type: ignore
            # type checker says, "Unnecessary isinstance call; "MazeProtocol" is always an instance of "MazeProtocol"PylancereportUnnecessaryIsInstance"
            # I mean yes, that's what I'm checking, because Python does not enforce strict types. Thanks anyway Pylance.
            return loaded
        else:
            # imported maze does not conform to MazeProtocol
            raise RuntimeError(
                (
                    f"Imported `maze` object from file {self.__path}"
                    " does not conform to `MazeProtocol` and"
                    " thus cannot be used as a maze object."
                )
            )

    def save(
        self,
        object: T,  # object has to conform to `Serializable` because `T` has to be `Serializable`
        key: str,
    ) -> None:
        # open a file handle within a context manager to not have to worry about closing the file
        with shelve.open(self.__path) as shelf:
            # save it to the file with given key
            # serialize it because `object` is of type `T` which conforms to `Serializable`
            shelf[key] = object.serialize()