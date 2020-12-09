#!python3.10

# queue position enum for specifying the position in the queue
from modules.data_structures.circular_queue._queue_position import QueuePosition

# linked list for enhanced queue
from modules.data_structures.linked_list.linked_list import LinkedList

# type hinting and some safety
from typing import Optional, TypeVar, Generic

T = TypeVar("T")


class CircularQueue(Generic[T]):
    """A queue object – first in, first out data structure designed in this case around readability, maintainability and efficiency.

    Args:
        Generic ([type]): The type of data this queue will store.

    Create a circular queue and test its length and maxSize
    >>> myQueue = CircularQueue[float](100)
    >>> len(myQueue)
    0

    Check maximum size of queue
    >>> myQueue._CircularQueue__maxSize     # accessing private attribute for testing
    100
    """

    # this is a circular queue. It is implemented as such
    __queue: LinkedList[Optional[T]]
    __maxSize: int
    __length: int
    __tail: int
    __head: int

    def __init__(self, maxSize: int):
        """Initialize an empty queue with maximum size.

        Args:
            maxSize (int): The maximum size of the queue.

        Initializing of a queue:
        >>> myQueue = CircularQueue[str](6)
        ... # Empty queue has correct length and initial items:
        >>> print(myQueue._CircularQueue__queue)       # accessing private attr for testing
        [None, None, None, None, None, None]

        Check the maximum size of the queue
        >>> myQueue._CircularQueue__maxSize     # accessing private attr for testing
        6
        """
        # initialize `self.queue` to an array of `-1` repeating `maxSize` number of times
        self.__queue = LinkedList[Optional[T]]([None] * maxSize)  # type: ignore     # for type hinting to work correctly
        # set `self._maxSize` to provided `maxSize` argument
        self.__maxSize = maxSize
        # set `self.__length` to 0, because there are no elements in our queue just yet
        self.__length = 0
        # and set both `self._tail` and `self._head` to `-1` as they don't point to anything yet
        self.__tail = -1
        self.__head = -1

    def __len__(self) -> int:
        return self.__length

    def enQueue(self, item: T) -> None:
        """Enqueue an item to the queue. Time complexity is O(1).

        Args:
            item (T): The item of type T to enqueue.

        Raises:
            Exception: Queue is full – it has reached the provided maximum size.

        Initialize a queue and add an acceptable number of items to it:
        >>> myQueue = CircularQueue[str](6)
        >>> myQueue.enQueue("Hello")
        >>> myQueue.enQueue("there,")
        >>> myQueue.enQueue("I")
        >>> myQueue.enQueue("am")
        >>> myQueue.enQueue("an")
        >>> myQueue.enQueue("octopus.")

        Check queue is full:
        >>> myQueue.isFull()
        True

        Try to add too many items:
        >>> myQueue.enQueue("overflow!")
        Traceback (most recent call last):
            ...
        Exception: Queue is full

        """

        # check if queue is full
        if not self.isFull():
            """
                The range for the head and tail pointer should be between 0 and `maxSize - 1`,
            hence we are using the logic that if we divide x by 5, then the remainder can
            never be greater than 5. In other words, it should be between 0 and 4. So apply
            this logic to the formulae:
                tail = (tail + 1) % maxSize
                head = (head + 1) % maxSize

                Observe that this helps us to avoid reinitializing tail and head to 0 when
            the queue becomes full.
            """
            self.__tail = (self.__tail + 1) % self.__maxSize
            self.__queue[self.__tail] = item
            self.__length += 1
            if self.__length == 1:
                self.__head = 0
        else:
            # queue is full! uh oh...
            raise Exception("Queue is full")

    def deQueue(self) -> T:
        """Dequeue the last item in the queue and return it. Time complexity is O(1).

        Raises:
            Exception: The queue is empty, so you can't dequeue anything.

        Returns:
            T: The dequeued item.

        Initialize a queue, add stuff, dequeue everything and test it all returns:
        >>> myQueue = CircularQueue[str](6)
        >>> myQueue.enQueue("Hello")
        >>> myQueue.enQueue("there,")
        >>> myQueue.enQueue("I")
        >>> myQueue.enQueue("am")
        >>> myQueue.enQueue("an")
        >>> myQueue.enQueue("octopus.")
        >>> # Now dequeue everything:
        >>> allTheElementsOfTheQueue = list[str]()
        >>> while myQueue.isEmpty() == False:
        ...     # dequeue an element...
        ...     dequeuedElement = myQueue.deQueue()
        ...     # ...and then print it. It is safe to print because the element is of type `str` (as we initialized our queue with the same element type).
        ...     allTheElementsOfTheQueue.append(dequeuedElement)
        >>> print(' '.join(allTheElementsOfTheQueue))
        Hello there, I am an octopus.

        The length of the queue should now be 0 as we dequeued everything:
        >>> len(myQueue)
        0
        """

        if self.isEmpty():
            # can't dequeue anything from an empty queue!
            raise Exception("Queue empty")

        # store in a temporary variable because if we return the value here, the rest of the function does not execute
        _dataToReturn = self.__queue[self.__head]

        self.__head = (self.__head + 1) % self.__maxSize
        # decrement `self.__length` by 1
        self.__length -= 1

        if self.isEmpty():
            # set head and tail to `-1` if the queue is empty
            self.__head = -1
            self.__tail = -1

        return (
            _dataToReturn
        )  # type:ignore because we previously guaranteed the list to not be empty with `self.isEmpty()``

    def get(self, position: QueuePosition) -> T:
        """Fetch an item from the front or the back of the queue without removing it from the queue

        Args:
            position (QueuePosition): The front or back of the queue – `QueuePosition.front` or `QueuePosition.back`

        Raises:
            Exception: Queue is empty and therefore cannot fetch any element from it
            Exception: Invalid QueuePosition given

        Returns:
            T: The fetched item

        Add some items to a queue and fetch the front item:
        >>> myQueue = CircularQueue[str](2)
        >>> myQueue.enQueue("Hello")
        >>> myQueue.enQueue("there")
        >>> myQueue.get(QueuePosition.front)
        'Hello'

        Fetch the rear item:
        >>> myQueue.get(QueuePosition.rear)
        'there'

        Add one item to a queue of length 1 and fetch the front:
        >>> myTinyQueue = CircularQueue[float](1)
        >>> myTinyQueue.enQueue(3.14159265)
        >>> myTinyQueue.get(QueuePosition.front)
        3.14159265

        Fetch the rear item from the 1-length queue:
        >>> myTinyQueue.get(QueuePosition.rear)
        3.14159265

        Add only one item to a queue of length 5 and fetching the front item:
        >>> myMediumQueue = CircularQueue[int](5)
        >>> myMediumQueue.enQueue(2)
        >>> myMediumQueue.get(QueuePosition.front)
        2

        Fetch the rear item from the 5-length queue with 1 item in:
        >>> myMediumQueue.get(QueuePosition.rear)
        2

        Using an invalid QueuePosition:
        >>> myQueue.get("hula hoops")
        Traceback (most recent call last):
            ...
        Exception: Queue position must be 'front' or 'rear'
        """
        if self.isEmpty():
            raise Exception("Queue is empty")

        if position == QueuePosition.front:
            return self.__queue[
                self.__head
            ]  # type:ignore   # already made sure the queue is not empty
        elif position == QueuePosition.rear:
            return self.__queue[
                self.__tail
            ]  # type:ignore   # again, it's guaranteed to be safe

        raise Exception("Queue position must be 'front' or 'rear'")

    def isEmpty(self) -> bool:
        """Check whether the queue is empty.

        Returns:
            bool: Whether or not the queue is empty.

        Initialize a queue and test if it is empty:
        >>> myQueue = CircularQueue[str](1)
        >>> myQueue.isEmpty()
        True
        >>> myQueue.enQueue("Foo")
        >>> myQueue.isEmpty()
        False
        """
        return self.__length == 0

    def isFull(self) -> bool:
        """Check whether the queue is full.

        Returns:
            bool: Whether or not the queue is full.

        Initialize a queue and check if the queue is full:
        >>> myQueue = CircularQueue[str](1)
        >>> myQueue.isFull()
        False

        Make it full and check it is now full:
        >>> myQueue.enQueue("octopus.")
        >>> myQueue.isFull()
        True
        """
        return self.__length == self.__maxSize
