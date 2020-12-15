from typing import Generic, List, Optional, TypeVar

T = TypeVar("T")


class Node(Generic[T]):
    """A node of a graph. Stores data and its connections.

    Args:
        Generic ([type]): The type of data the node will store.
    """

    # This could easily be made into a Tuple rather than a whole new class but for debugging purposes, I chose to make this a class.

    data: Optional[
        T
    ]  # this node's data  - public because the graph may want to set its data again
    connections: list[
        int
    ]  # pointers of this node's connections   – public bc it needs to be read by the graph
    visited: bool = (
        False  # a helper variable to assist in traversals of a graph of nodes
    )

    def __init__(self, data: Optional[T], connections: list[int] = list[int]()) -> None:
        """Constructor for a binary tree node.

        Args:
            data (T): This node's data, e.g. 'Barry'.
            connections (list[int], optional): The list of pointers that are connections of this node. Defaults to an emply list[int]().
        """
        self.data = data
        self.connections = connections

    def __repr__(self) -> str:
        """Return a string representation of this object

        Returns:
            str: The string representation of the object, for example:
        ```
        "Alice -> (1, 4)"
        ```
        """
        # For example, "Bob -> [0, 4]"
        return str(
            str(self.data) + " -> [" + ", ".join(map(str, self.connections)) + "]"
        )

    def clone(self) -> "Node[T]":
        #  make sure to clone by value, not reference.
        connections: List[int] = [x for x in self.connections]
        return Node[T](self.data, connections)