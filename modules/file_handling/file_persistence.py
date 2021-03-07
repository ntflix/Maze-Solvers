import dbm
from modules.file_handling.serializable import Serializable
from typing import Any, Generic, TypeVar
import logging
import shelve

T = TypeVar("T", bound=Serializable)  # T has to conform to Serializable


class FilePersistence(Generic[T]):
    __path: str

    def __init__(self, path: str):
        self.__path = path

    def load(self, key: str) -> Any:
        # remove '.db' from end of path so the Shelve module can load it properly (the Shelve module auto adds extension…)
        # if file ends with ".db"
        if self.__path[-3:] == ".db":
            # then remove the last part
            self.__path = self.__path[:-3]

        logging.debug(f"Loading object from '{self.__path}'")
        # define `loaded` variable here to be used in function scope. Type is 'any' because we do not check the type of the data.
        loaded: Any

        #  open the file within a context manager
        try:
            # sheve.open(self.__path, flag="r")  # open in read mode
            with shelve.open(self.__path, flag="r") as shelf:
                # load from file
                loaded = shelf[key]
        except dbm.error as error:  # there was an error with the loading of the file
            # make a nice error message :)
            errorMessage = f"Could not load file from {self.__path}: {error}."
            # log the error
            logging.error(errorMessage)
            # aaand raise a not so nice error with the nice message for the happy user
            raise FileNotFoundError(errorMessage)

        return loaded

    def save(
        self,
        object: T,  # object has to conform to `Serializable` because `T` has to be `Serializable`
        key: str,
    ) -> None:
        # log saving file
        logging.debug(f"Saving object '{object}' to '{self.__path}' with key '{key}'.")
        # open a file handle within a context manager to not have to worry about closing the file
        with shelve.open(self.__path, flag="c") as shelf:  # open in create/write mode
            logging.debug(f"Opened shelve file handle at {self.__path}")
            # save it to the file with given key
            # serialize it because `object` is of type `T` which conforms to `Serializable`
            shelf[key] = object.serialize()

        shelf.close()

        logging.debug(f"Saved object '{object}' to '{self.__path}' with key '{key}'.")