from typing import List, Optional, TypeVar, Generic

T = TypeVar("T")


class Stack(Generic[T]):
    __stack: List[Optional[T]] = list()
    __top = -1

    def pop(self) -> T:
        if not self.isEmpty():
            item = self.__stack[self.__top]
            self.__stack[self.__top] = None
            self.__top -= 1
            return item  # type: ignore – cannot be None because we checked whether self.__isEmpty()
        raise IndexError("Stack empty")

    def peek(self) -> T:
        if not self.isEmpty():
            return self.__stack[self.__top]  # type: ignore – cannot be None because we checked whether self.__isEmpty()
        raise IndexError("Stack empty")

    def push(self, item: T) -> None:
        self.__top += 1
        if len(self.__stack) <= self.__top:
            self.__stack.append(item)
        else:
            self.__stack[self.__top] = item

    def isEmpty(self) -> bool:
        return self.__top == -1

    def __len__(self) -> int:
        return self.__top + 1