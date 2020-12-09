from typing import Generic, TypeVar, Optional

T = TypeVar("T")


class LinkedListNode(Generic[T]):
    """A node for a linked list object

    Args:
        Generic ([type]): The type of data this node will store
    """

    data: T  # this node's data
    # the pointer of the next node  # variable type is in quotes because we are using forward referencing here to avoid recursive typing
    nextNode: Optional["LinkedListNode[T]"]

    def __init__(self, data: T, nextNode: Optional["LinkedListNode[T]"] = None) -> None:
        """Constructor for a `LinkedListNode`

        Args:
            data (T): The data for this node to store
            next (int): The integer pointer of the next `LinkedListNode`

        Instantiating a `LinkedListNode`:
        >>> myLinkedListNode = LinkedListNode[int](65536, nextNode = 5)     # instantiate a LinkedListNode object
        >>> myLinkedListNode.data
        65536
        >>> myLinkedListNode.nextNode
        5

        """
        self.data = data
        self.nextNode = nextNode

    def __repr__(self) -> str:
        """Generate a string representation of this object
        For example, "'Barry' -> 4" for an object where `data` = 'Barry' and `nextPointer` = 4

        Returns:
            str: the string representation of the object

        >>> LinkedListNode[str](data = "Gareth", nextNode = 2)
        Gareth (2)
        """
        return "{} ({})".format(str(self.data), str(self.nextNode))

    def clone(self) -> "LinkedListNode[T]":
        """Recursively clone an object to overcome Python's pass-by-reference argument types.
        Basically used to force Python to pass by value rather than reference.

        Returns:
            LinkedListNode[T]: this object, cloned.
        """
        node = LinkedListNode[T](self.data)

        if self.nextNode is not None:
            # call this recursively to get all the values for the nodes while not copying by reference
            node.nextNode = self.nextNode.clone()
        else:
            #  got to the end of the chain of nodes
            node.nextNode = None

        return node