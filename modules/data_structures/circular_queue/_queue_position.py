from enum import Enum

class QueuePosition(Enum):
    """An enum for either the front or rear of a queue

    Args:
        Enum ([type]): Automatically provided by the enum module.

    Example usage:
        `QueuePosition.front`
        `QueuePosition.rear`

    Check QueuePosition initializes properly
    >>> front = QueuePosition.front
    >>> print(front)
    QueuePosition.front
    >>> rear = QueuePosition.rear
    >>> print(rear)
    QueuePosition.rear
    """

    front = 0
    rear = 1
