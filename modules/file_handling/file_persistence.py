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
        logging.debug(f"Loading object from '{self.__path}'")
        # define `loaded` variable here to be used in function scope
        loaded: T

        #  open the file within a context manager
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

        logging.debug(
            f"Loaded object from '{self.__path}' with key '{key}' as '{loaded}'."
        )

        return loaded

    def save(
        self,
        object: T,  # object has to conform to `Serializable` because `T` has to be `Serializable`
        key: str,
    ) -> None:
        # log saving file
        logging.debug(f"Saving object '{object}' to '{self.__path}' with key '{key}'.")
        # open a file handle within a context manager to not have to worry about closing the file
        with shelve.open(self.__path) as shelf:
            logging.debug(f"Opened shelve file handle at {self.__path}")
            # save it to the file with given key
            # serialize it because `object` is of type `T` which conforms to `Serializable`
            shelf[key] = object.serialize()

        logging.debug(f"Saved object '{object}' to '{self.__path}' with key '{key}'.")