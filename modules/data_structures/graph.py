#!python3.10

from typing import Generic, TypeVar

T = TypeVar('T')

class Node(Generic[T]):
    # This could easily be made into a `Tuple` rather than a whole new class but for debugging purposes, I chose to make this a class.

    data: T     # this node's data
    connections: list[int]   # pointers of this node's connections

    def __init__(self, data: T, connections: list[int] = list[int]()) -> None:
        """Constructor for a binary tree node.

        Args:
            data (T): This node's data, e.g. 'Barry'.
            connections (list[int], optional): The list of pointers that are connections of this node. Defaults to an emply list[int]().
        """
        self.data = data
        self.connections = connections

class Graph(Generic[T]):
    """A binary graph of type {T}."""

    values: list[T]
    connections = list[int]()

    nodes: list[Node[T]]    # a helper variable, temporarily used 

    def __init__(self):
        """Constructor for a binary tree of type {T}.

        Args:
            type (T): The value type of the values of the nodes of the tree. For example, a tree storing names would have a value type of {str}.

        Returns:
            None.
        """
        self.values: list[T] = []       # Initialize self.values to an empty list to remove old values
        self.nodes: list[Node[T]] = []  # Initialize self.nodes to an empty list

        for value in self.values:
            if self.values.count(value) > 1:
                # There are duplicate values in the tree
                print("Invalid tree. Duplicate values must not exist. Value: " + str(value))
                exit(1)
    
    def setNodes(self, values: list[T], connectionsPointers: list[list[int]]) -> None:
        """Give a Tree object some nodes.

        Args:
            values (List[T]): the value of each node
            leftPointers (List[int]): the left pointer of each node, where index is the node number
            rightPointers (List[int]): the right pointer of each node, where index is the node number
        """

        self.values = values                    # set `self.values` to the provided values
        self.connections = connectionsPointers  # and set `self.connections` to provided connections

        for i in range(len(values)):
            thisNode: Node[T] = Node(data = values[i], connections = connectionsPointers[i])    # make new Node with this value's data and left and right pointers
            self.nodes.append(thisNode)     # append new node to `self.nodes`

    # TODO: Implement breadth first traversal.

    def _exists(self, nodePointer: int) -> bool:
        """Determine whether or not a pointer points to a valid node.

        Args:
            nodePointer (int): The index of the node the pointer points to.

        Returns:
            bool: Whether the pointer is valid.
        """

        return not nodePointer in [-1]